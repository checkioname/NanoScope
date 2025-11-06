"""
Analisador médico usando modelos leves e fáceis de usar.
Opções: OpenAI API, Ollama local, ou Hugging Face Transformers pequenos.
"""

import json
import requests
from typing import Dict, List, Any
import os

class LightweightMedicalAnalyzer:
    def __init__(self, model_type="openai"):
        """
        Inicializa com diferentes opções de modelo:
        - "openai": OpenAI GPT (requer API key)
        - "ollama": Ollama local (requer Ollama instalado)
        - "huggingface": Modelo pequeno do HuggingFace
        - "simple": Análise baseada em regras (fallback)
        """
        self.model_type = model_type
        print(f"[LIGHTWEIGHT ANALYZER] Inicializando com modelo: {model_type}")
        
        if model_type == "openai":
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
            if not self.openai_api_key:
                print("[LIGHTWEIGHT ANALYZER] OPENAI_API_KEY não encontrada, usando fallback")
                self.model_type = "simple"
        
        elif model_type == "ollama":
            # Testar se Ollama está disponível
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code != 200:
                    raise Exception("Ollama não disponível")
                print("[LIGHTWEIGHT ANALYZER] Ollama detectado e funcionando")
            except:
                print("[LIGHTWEIGHT ANALYZER] Ollama não disponível, usando fallback")
                self.model_type = "simple"
        
        elif model_type == "huggingface":
            try:
                from transformers import pipeline
                # Usar um modelo pequeno e rápido
                self.analyzer = pipeline(
                    "text-generation", 
                    model="microsoft/DialoGPT-small",  # Modelo pequeno (~117MB)
                    max_length=512
                )
                print("[LIGHTWEIGHT ANALYZER] Modelo HuggingFace carregado")
            except ImportError:
                print("[LIGHTWEIGHT ANALYZER] Transformers não disponível, usando fallback")
                self.model_type = "simple"
            except Exception as e:
                print(f"[LIGHTWEIGHT ANALYZER] Erro ao carregar HuggingFace: {e}, usando fallback")
                self.model_type = "simple"
    
    def generate_medical_analysis(self, cell_features: List[Dict], global_metrics: Dict, 
                                image_context: str = "tissue sample") -> Dict[str, Any]:
        """Gera análise médica usando o modelo escolhido"""
        
        # Preparar dados para o prompt
        analysis_data = self._prepare_analysis_data(cell_features, global_metrics, image_context)
        
        if self.model_type == "openai":
            return self._analyze_with_openai(analysis_data)
        elif self.model_type == "ollama":
            return self._analyze_with_ollama(analysis_data)
        elif self.model_type == "huggingface":
            return self._analyze_with_huggingface(analysis_data)
        else:
            return self._analyze_with_rules(analysis_data)
    
    def _prepare_analysis_data(self, cell_features, global_metrics, image_context):
        """Prepara dados para análise"""
        return {
            "total_cells": global_metrics.get('total_cells', 0),
            "malignant_cells": global_metrics.get('potentially_malignant_cells', 0),
            "malignancy_percentage": global_metrics.get('malignancy_percentage', 0),
            "quality_score": global_metrics.get('image_quality_score', 0),
            "context": image_context,
            "cell_count": len(cell_features) if cell_features else 0
        }
    
    def _analyze_with_openai(self, data):
        """Análise usando OpenAI GPT"""
        try:
            prompt = f"""
Como patologista especializado, analise os seguintes dados citológicos:

Dados da amostra:
- Total de células: {data['total_cells']}
- Células atípicas: {data['malignant_cells']} ({data['malignancy_percentage']:.1f}%)
- Qualidade da imagem: {data['quality_score']:.1f}/100
- Contexto: {data['context']}

Forneça uma análise médica estruturada em português incluindo:
1. Interpretação dos achados
2. Diagnóstico diferencial
3. Recomendações clínicas
4. Avaliação de risco

Seja conciso e profissional.
"""

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-3.5-turbo",  # Modelo mais barato
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 500,
                    "temperature": 0.3
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis_text = result['choices'][0]['message']['content']
                return self._parse_openai_response(analysis_text, data)
            else:
                print(f"[LIGHTWEIGHT ANALYZER] Erro OpenAI: {response.status_code}")
                return self._analyze_with_rules(data)
                
        except Exception as e:
            print(f"[LIGHTWEIGHT ANALYZER] Erro OpenAI: {e}")
            return self._analyze_with_rules(data)
    
    def _analyze_with_ollama(self, data):
        """Análise usando Ollama local"""
        try:
            prompt = f"""
Você é um patologista. Analise estes dados citológicos:

Células totais: {data['total_cells']}
Células atípicas: {data['malignant_cells']} ({data['malignancy_percentage']:.1f}%)
Qualidade: {data['quality_score']:.1f}/100

Forneça:
1. Interpretação
2. Diagnóstico
3. Recomendações
4. Risco (Alto/Moderado/Baixo)

Seja conciso.
"""

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2:1b",  # Modelo pequeno e rápido
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 300
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis_text = result.get('response', '')
                return self._parse_ollama_response(analysis_text, data)
            else:
                print(f"[LIGHTWEIGHT ANALYZER] Erro Ollama: {response.status_code}")
                return self._analyze_with_rules(data)
                
        except Exception as e:
            print(f"[LIGHTWEIGHT ANALYZER] Erro Ollama: {e}")
            return self._analyze_with_rules(data)
    
    def _analyze_with_huggingface(self, data):
        """Análise usando HuggingFace"""
        try:
            prompt = f"Análise médica: {data['total_cells']} células, {data['malignancy_percentage']:.1f}% atípicas."
            
            result = self.analyzer(prompt, max_length=200, num_return_sequences=1)
            analysis_text = result[0]['generated_text']
            
            return self._parse_huggingface_response(analysis_text, data)
            
        except Exception as e:
            print(f"[LIGHTWEIGHT ANALYZER] Erro HuggingFace: {e}")
            return self._analyze_with_rules(data)
    
    def _analyze_with_rules(self, data):
        """Análise baseada em regras (fallback)"""
        malignancy_pct = data['malignancy_percentage']
        total_cells = data['total_cells']
        quality_score = data['quality_score']
        
        # Gerar análise baseada em regras
        if malignancy_pct > 30:
            analysis = f"""
ANÁLISE CITOLÓGICA - ALTO RISCO

Foram analisadas {total_cells} células, das quais {data['malignant_cells']} ({malignancy_pct:.1f}%) apresentam características atípicas significativas.

INTERPRETAÇÃO:
Presença de células com alterações morfológicas importantes, incluindo irregularidades nucleares, aumento da razão núcleo/citoplasma e variabilidade textural. Estes achados são sugestivos de processo neoplásico.

RECOMENDAÇÕES:
1. Encaminhamento urgente para oncologista
2. Biópsia para confirmação histopatológica
3. Estadiamento completo se confirmada malignidade
4. Avaliação multidisciplinar

RISCO: Alto - Investigação adicional urgente"""

        elif malignancy_pct > 10:
            analysis = f"""
ANÁLISE CITOLÓGICA - RISCO MODERADO

Análise de {total_cells} células revelou {data['malignant_cells']} ({malignancy_pct:.1f}%) com características atípicas moderadas.

INTERPRETAÇÃO:
Presença de alterações celulares que podem representar processo reativo, displásico ou neoplásico inicial. Requer acompanhamento cuidadoso.

RECOMENDAÇÕES:
1. Acompanhamento clínico em 3-6 meses
2. Repetir citologia se per sistência dos sintomas
3. Correlação com exames complementares
4. Considerar biópsia se progressão

RISCO: Moderado - Acompanhamento necessário"""

        else:
            analysis = f"""
ANÁLISE CITOLÓGICA - BAIXO RISCO

Exame de {total_cells} células com {malignancy_pct:.1f}% de atipias, dentro dos limites da normalidade.

INTERPRETAÇÃO:
Células apresentam morfologia predominantemente normal, sem evidências de malignidade. Achados compatíveis com tecido benigno.

RECOMENDAÇÕES:
1. Seguimento de rotina conforme protocolo
2. Manter rastreamento preventivo regular
3. Retorno se novos sintomas

RISCO: Baixo - Achados normais"""

        # Calcular confiança
        confidence = min((quality_score / 100 + min(total_cells / 50, 1.0)) / 2, 1.0)
        
        return {
            "medical_analysis": analysis.strip(),
            "diagnosis_summary": f"Análise de {total_cells} células com {malignancy_pct:.1f}% de atipias",
            "recommendations": self._extract_recommendations(analysis),
            "confidence_score": confidence,
            "key_findings": [
                f"{total_cells} células analisadas",
                f"{malignancy_pct:.1f}% de atipias",
                f"Qualidade: {quality_score:.1f}/100"
            ],
            "risk_assessment": self._get_risk_level(malignancy_pct)
        }
    
    def _parse_openai_response(self, text, data):
        """Parse da resposta do OpenAI"""
        return {
            "medical_analysis": text,
            "diagnosis_summary": f"Análise de {data['total_cells']} células com {data['malignancy_percentage']:.1f}% de atipias",
            "recommendations": self._extract_recommendations(text),
            "confidence_score": 0.9,  # Alta confiança para OpenAI
            "key_findings": [
                f"{data['total_cells']} células analisadas",
                f"{data['malignancy_percentage']:.1f}% de atipias",
                "Análise por IA médica especializada"
            ],
            "risk_assessment": self._get_risk_level(data['malignancy_percentage'])
        }
    
    def _parse_ollama_response(self, text, data):
        """Parse da resposta do Ollama"""
        return {
            "medical_analysis": text,
            "diagnosis_summary": f"Análise de {data['total_cells']} células com {data['malignancy_percentage']:.1f}% de atipias",
            "recommendations": self._extract_recommendations(text),
            "confidence_score": 0.8,  # Boa confiança para Ollama
            "key_findings": [
                f"{data['total_cells']} células analisadas",
                f"{data['malignancy_percentage']:.1f}% de atipias",
                "Análise por modelo local"
            ],
            "risk_assessment": self._get_risk_level(data['malignancy_percentage'])
        }
    
    def _parse_huggingface_response(self, text, data):
        """Parse da resposta do HuggingFace"""
        return {
            "medical_analysis": text,
            "diagnosis_summary": f"Análise de {data['total_cells']} células com {data['malignancy_percentage']:.1f}% de atipias",
            "recommendations": "Consulte um especialista para interpretação detalhada",
            "confidence_score": 0.6,  # Confiança moderada
            "key_findings": [
                f"{data['total_cells']} células analisadas",
                f"{data['malignancy_percentage']:.1f}% de atipias"
            ],
            "risk_assessment": self._get_risk_level(data['malignancy_percentage'])
        }
    
    def _extract_recommendations(self, text):
        """Extrai recomendações do texto"""
        if "RECOMENDAÇÕES" in text:
            parts = text.split("RECOMENDAÇÕES")[1].split("RISCO")[0]
            return parts.strip()
        return "Consulte um especialista para recomendações específicas"
    
    def _get_risk_level(self, malignancy_pct):
        """Determina nível de risco"""
        if malignancy_pct > 30:
            return "Alto risco - Investigação adicional urgente"
        elif malignancy_pct > 10:
            return "Risco moderado - Acompanhamento recomendado"
        else:
            return "Baixo risco - Achados normais"
