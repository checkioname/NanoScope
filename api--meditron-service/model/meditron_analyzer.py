import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import json
from typing import Dict, List, Any

class MeditronAnalyzer:
    def __init__(self, model_name="epfl-llm/meditron-7b"):
        """
        Inicializa o analisador Meditron.
        Usa Meditron-7B em vez do 70B para melhor performance.
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Configuração para quantização (reduz uso de memória)
        self.quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
        
        self.tokenizer = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Carrega o modelo Meditron com otimizações"""
        try:
            print(f"[MEDITRON] Carregando modelo {self.model_name}...")
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Adicionar pad_token se não existir
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Carregar modelo com quantização
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                quantization_config=self.quantization_config,
                device_map="auto",
                torch_dtype=torch.float16,
                trust_remote_code=True
            )
            
            print(f"[MEDITRON] Modelo carregado com sucesso no device: {self.device}")
            
        except Exception as e:
            print(f"[MEDITRON] Erro ao carregar modelo: {e}")
            # Fallback para modelo menor ou mock
            self._load_fallback_model()
    
    def _load_fallback_model(self):
        """Modelo de fallback caso o Meditron não carregue"""
        print("[MEDITRON] Usando modelo de fallback (mock)")
        self.model = None
        self.tokenizer = None
    
    def _format_cell_data(self, cell_features: List[Dict], global_metrics: Dict) -> str:
        """Formata os dados celulares para o prompt médico"""
        
        # Resumo global
        summary = f"""
ANÁLISE CITOLÓGICA - DADOS QUANTITATIVOS:

Métricas Globais:
- Total de células analisadas: {global_metrics.get('total_cells', 0)}
- Células com características suspeitas: {global_metrics.get('potentially_malignant_cells', 0)}
- Percentual de malignidade: {global_metrics.get('malignancy_percentage', 0):.1f}%
- Densidade celular: {global_metrics.get('cell_density_per_mm2', 0):.2f} células/mm²
- Tamanho médio celular: {global_metrics.get('mean_cell_size', 0):.1f} pixels
- Variabilidade de tamanho: {global_metrics.get('cell_size_variability', 0):.2f}
- Qualidade da imagem: {global_metrics.get('image_quality_score', 0):.1f}/100

Características Celulares Individuais:
"""
        
        # Adicionar dados de células suspeitas
        suspicious_cells = [cell for cell in cell_features if cell.get('is_potentially_malignant', False)]
        
        if suspicious_cells:
            summary += f"\nCélulas com características atípicas ({len(suspicious_cells)} encontradas):\n"
            for i, cell in enumerate(suspicious_cells[:5]):  # Limitar a 5 células
                summary += f"""
Célula {cell.get('cell_id', i+1)}:
- Área: {cell.get('area', 0):.1f} pixels²
- Circularidade: {cell.get('circularity', 0):.2f} (normal: 0.7-1.0)
- Excentricidade: {cell.get('eccentricity', 0):.2f}
- Razão núcleo/citoplasma: {cell.get('nucleus_cytoplasm_ratio', 0):.2f}
- Intensidade média: {cell.get('mean_intensity', 0):.1f}
- Variabilidade textural: {cell.get('texture_contrast', 0):.1f}
"""
        
        return summary
    
    def generate_medical_analysis(self, cell_features: List[Dict], global_metrics: Dict, 
                                image_context: str = "tissue sample") -> Dict[str, Any]:
        """
        Gera análise médica baseada nos dados do Cellpose
        """
        
        if self.model is None:
            return self._generate_mock_analysis(cell_features, global_metrics)
        
        try:
            # Formatar dados para o prompt
            cell_data = self._format_cell_data(cell_features, global_metrics)
            
            # Criar prompt médico estruturado
            prompt = f"""Como um patologista especializado, analise os seguintes dados citológicos quantitativos e forneça uma avaliação médica detalhada:

{cell_data}

Contexto da amostra: {image_context}

Por favor, forneça uma análise estruturada incluindo:

1. INTERPRETAÇÃO DOS ACHADOS:
2. DIAGNÓSTICO DIFERENCIAL:
3. RECOMENDAÇÕES CLÍNICAS:
4. AVALIAÇÃO DE RISCO:
5. CONCLUSÃO:

Análise:"""

            # Tokenizar e gerar resposta
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs.input_ids,
                    max_new_tokens=512,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decodificar resposta
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            analysis_text = response[len(prompt):].strip()
            
            # Processar e estruturar a resposta
            return self._parse_medical_response(analysis_text, global_metrics)
            
        except Exception as e:
            print(f"[MEDITRON] Erro na geração: {e}")
            return self._generate_mock_analysis(cell_features, global_metrics)
    
    def _parse_medical_response(self, analysis_text: str, global_metrics: Dict) -> Dict[str, Any]:
        """Parse da resposta do modelo em estrutura organizada"""
        
        # Extrair seções principais
        sections = {
            "medical_analysis": analysis_text,
            "diagnosis_summary": "",
            "recommendations": "",
            "risk_assessment": "",
            "key_findings": [],
            "confidence_score": 0.0
        }
        
        # Calcular score de confiança baseado na qualidade dos dados
        quality_score = global_metrics.get('image_quality_score', 0) / 100
        cell_count_score = min(global_metrics.get('total_cells', 0) / 50, 1.0)
        sections["confidence_score"] = (quality_score + cell_count_score) / 2
        
        # Extrair achados principais
        malignancy_pct = global_metrics.get('malignancy_percentage', 0)
        total_cells = global_metrics.get('total_cells', 0)
        
        sections["key_findings"] = [
            f"Total de {total_cells} células analisadas",
            f"Taxa de atipias: {malignancy_pct:.1f}%",
            f"Qualidade da amostra: {global_metrics.get('image_quality_score', 0):.1f}/100"
        ]
        
        # Avaliação de risco simplificada
        if malignancy_pct > 30:
            sections["risk_assessment"] = "Alto risco - Requer investigação adicional urgente"
        elif malignancy_pct > 10:
            sections["risk_assessment"] = "Risco moderado - Acompanhamento recomendado"
        else:
            sections["risk_assessment"] = "Baixo risco - Achados dentro da normalidade"
        
        return sections
    
    def _generate_mock_analysis(self, cell_features: List[Dict], global_metrics: Dict) -> Dict[str, Any]:
        """Gera análise mock quando o modelo não está disponível"""
        
        total_cells = global_metrics.get('total_cells', 0)
        malignant_cells = global_metrics.get('potentially_malignant_cells', 0)
        malignancy_pct = global_metrics.get('malignancy_percentage', 0)
        quality_score = global_metrics.get('image_quality_score', 0)
        
        analysis = f"""
ANÁLISE CITOLÓGICA AUTOMATIZADA

ACHADOS QUANTITATIVOS:
- Foram analisadas {total_cells} células na amostra
- {malignant_cells} células apresentaram características atípicas ({malignancy_pct:.1f}%)
- Qualidade da imagem: {quality_score:.1f}/100

INTERPRETAÇÃO:
"""
        
        if malignancy_pct > 30:
            analysis += """
Presença significativa de células com características atípicas. Observa-se:
- Irregularidades na morfologia nuclear
- Variações no tamanho celular
- Alterações na razão núcleo/citoplasma

RECOMENDAÇÕES:
- Revisão por patologista experiente
- Considerar biópsia adicional se indicado clinicamente
- Correlação com dados clínicos e radiológicos
"""
            risk = "Alto risco"
        elif malignancy_pct > 10:
            analysis += """
Presença moderada de células atípicas. Características observadas:
- Algumas irregularidades morfológicas
- Variabilidade celular dentro de limites aceitáveis

RECOMENDAÇÕES:
- Acompanhamento clínico regular
- Repetir exame em 6 meses se indicado
"""
            risk = "Risco moderado"
        else:
            analysis += """
Células apresentam morfologia predominantemente normal.
- Características citológicas dentro dos padrões esperados
- Ausência de atipias significativas

RECOMENDAÇÕES:
- Seguimento de rotina conforme protocolo clínico
"""
            risk = "Baixo risco"
        
        return {
            "medical_analysis": analysis.strip(),
            "diagnosis_summary": f"Análise de {total_cells} células com {malignancy_pct:.1f}% de atipias",
            "recommendations": "Correlacionar com achados clínicos e seguir protocolo institucional",
            "confidence_score": min(quality_score / 100 + (total_cells / 100), 1.0),
            "key_findings": [
                f"{total_cells} células analisadas",
                f"{malignancy_pct:.1f}% de células atípicas",
                f"Qualidade: {quality_score:.1f}/100"
            ],
            "risk_assessment": risk
        }

