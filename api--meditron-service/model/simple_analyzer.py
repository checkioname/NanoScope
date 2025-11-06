"""
Analisador médico simplificado que não depende de modelos pesados.
Usa análise baseada em regras para gerar relatórios médicos.
"""

from typing import Dict, List, Any

class SimpleMedicalAnalyzer:
    def __init__(self):
        """Inicializa o analisador simplificado"""
        print("[SIMPLE ANALYZER] Inicializando analisador médico simplificado...")
        
    def generate_medical_analysis(self, cell_features: List[Dict], global_metrics: Dict, 
                                image_context: str = "tissue sample") -> Dict[str, Any]:
        """
        Gera análise médica baseada em regras clínicas estabelecidas
        """
        
        if not global_metrics:
            return self._generate_error_response()
        
        try:
            total_cells = global_metrics.get('total_cells', 0)
            malignant_cells = global_metrics.get('potentially_malignant_cells', 0)
            malignancy_pct = global_metrics.get('malignancy_percentage', 0)
            quality_score = global_metrics.get('image_quality_score', 0)
            
            # Gerar análise médica estruturada
            analysis = self._generate_detailed_analysis(
                total_cells, malignant_cells, malignancy_pct, quality_score, cell_features
            )
            
            # Gerar resumo do diagnóstico
            diagnosis_summary = f"Análise citológica de {total_cells} células com {malignancy_pct:.1f}% de atipias detectadas"
            
            # Gerar recomendações
            recommendations = self._generate_clinical_recommendations(malignancy_pct, quality_score)
            
            # Calcular score de confiança
            confidence_score = self._calculate_confidence_score(total_cells, quality_score)
            
            # Gerar achados principais
            key_findings = self._generate_key_findings(total_cells, malignancy_pct, quality_score)
            
            # Avaliação de risco
            risk_assessment = self._generate_risk_assessment(malignancy_pct)
            
            print(f"[SIMPLE ANALYZER] Análise gerada - Células: {total_cells}, Risco: {risk_assessment}")
            
            return {
                "medical_analysis": analysis,
                "diagnosis_summary": diagnosis_summary,
                "recommendations": recommendations,
                "confidence_score": confidence_score,
                "key_findings": key_findings,
                "risk_assessment": risk_assessment
            }
            
        except Exception as e:
            print(f"[SIMPLE ANALYZER] Erro na análise: {e}")
            return self._generate_error_response()
    
    def _generate_detailed_analysis(self, total_cells, malignant_cells, malignancy_pct, 
                                  quality_score, cell_features):
        """Gera análise médica detalhada"""
        
        analysis = f"""
RELATÓRIO DE ANÁLISE CITOLÓGICA AUTOMATIZADA

═══════════════════════════════════════════════════════════════

DADOS QUANTITATIVOS:
• Total de células analisadas: {total_cells}
• Células com características atípicas: {malignant_cells} ({malignancy_pct:.1f}%)
• Qualidade da amostra: {quality_score:.1f}/100

INTERPRETAÇÃO MORFOLÓGICA:
{self._get_morphological_interpretation(malignancy_pct)}

ANÁLISE CITOLÓGICA DETALHADA:
{self._get_detailed_cytological_analysis(malignancy_pct, cell_features)}

CORRELAÇÃO CLÍNICA:
{self._get_clinical_correlation(malignancy_pct, quality_score)}

CONCLUSÃO:
{self._get_conclusion(malignancy_pct)}
"""
        return analysis.strip()
    
    def _get_morphological_interpretation(self, malignancy_pct):
        """Interpretação morfológica baseada no percentual de malignidade"""
        if malignancy_pct > 30:
            return """Observa-se presença significativa de células com características atípicas.
As alterações morfológicas incluem:
- Irregularidades na forma e tamanho nuclear
- Aumento da razão núcleo/citoplasma
- Variabilidade na distribuição da cromatina
- Possíveis figuras mitóticas atípicas

Estas características sugerem processo neoplásico que requer investigação adicional."""

        elif malignancy_pct > 10:
            return """Presença moderada de células com características atípicas.
As alterações observadas incluem:
- Discretas irregularidades nucleares
- Leve aumento da razão núcleo/citoplasma
- Variabilidade celular dentro de limites aceitáveis

Achados compatíveis com processo reativo ou displásico leve."""

        else:
            return """Células apresentam morfologia predominantemente normal.
Características observadas:
- Núcleos regulares com cromatina homogênea
- Razão núcleo/citoplasma preservada
- Ausência de atipias significativas

Morfologia citológica dentro dos padrões de normalidade."""

    def _get_detailed_cytological_analysis(self, malignancy_pct, cell_features):
        """Análise citológica detalhada"""
        if not cell_features:
            return "Análise individual das células não disponível."
        
        suspicious_cells = [cell for cell in cell_features if cell.get('is_potentially_malignant', False)]
        
        if not suspicious_cells:
            return "Todas as células analisadas apresentam características morfológicas normais."
        
        analysis = f"Das células analisadas, {len(suspicious_cells)} apresentam características atípicas:\n\n"
        
        # Analisar até 3 células suspeitas
        for i, cell in enumerate(suspicious_cells[:3]):
            cell_id = cell.get('cell_id', i+1)
            area = cell.get('area', 0)
            circularity = cell.get('circularity', 0)
            nc_ratio = cell.get('nucleus_cytoplasm_ratio', 0)
            
            analysis += f"• Célula {cell_id}:\n"
            analysis += f"  - Área: {area:.1f} pixels² "
            
            if area > 1000:
                analysis += "(aumentada)"
            elif area < 50:
                analysis += "(diminuída)"
            else:
                analysis += "(normal)"
            
            analysis += f"\n  - Circularidade: {circularity:.2f} "
            
            if circularity < 0.7:
                analysis += "(irregular)"
            else:
                analysis += "(preservada)"
            
            analysis += f"\n  - Razão N/C: {nc_ratio:.2f} "
            
            if nc_ratio > 0.3:
                analysis += "(aumentada - suspeita)"
            else:
                analysis += "(normal)"
            
            analysis += "\n\n"
        
        if len(suspicious_cells) > 3:
            analysis += f"... e mais {len(suspicious_cells) - 3} células com características similares."
        
        return analysis

    def _get_clinical_correlation(self, malignancy_pct, quality_score):
        """Correlação clínica"""
        correlation = "A interpretação destes achados deve ser correlacionada com:\n"
        correlation += "• História clínica do paciente\n"
        correlation += "• Exames de imagem (se disponíveis)\n"
        correlation += "• Marcadores tumorais (se indicados)\n"
        
        if quality_score < 70:
            correlation += "\nNOTA: A qualidade da amostra está abaixo do ideal, "
            correlation += "o que pode limitar a precisão da análise."
        
        if malignancy_pct > 20:
            correlation += "\nRecomenda-se discussão em equipe multidisciplinar "
            correlation += "para definição da conduta terapêutica."
        
        return correlation

    def _get_conclusion(self, malignancy_pct):
        """Conclusão do laudo"""
        if malignancy_pct > 30:
            return """CONCLUSÃO: Presença de células com características citológicas atípicas 
significativas, sugerindo processo neoplásico. Recomenda-se confirmação 
histopatológica e estadiamento adequado."""

        elif malignancy_pct > 10:
            return """CONCLUSÃO: Presença de atipias celulares de significado indeterminado. 
Recomenda-se acompanhamento clínico e repetição do exame se clinicamente indicado."""

        else:
            return """CONCLUSÃO: Citologia dentro dos padrões de normalidade. 
Manter seguimento de rotina conforme protocolo clínico."""

    def _generate_clinical_recommendations(self, malignancy_pct, quality_score):
        """Gera recomendações clínicas"""
        recommendations = "RECOMENDAÇÕES CLÍNICAS:\n\n"
        
        if malignancy_pct > 30:
            recommendations += "1. Encaminhamento urgente para oncologista\n"
            recommendations += "2. Biópsia para confirmação histopatológica\n"
            recommendations += "3. Estadiamento completo se confirmada malignidade\n"
            recommendations += "4. Avaliação multidisciplinar\n"
        elif malignancy_pct > 10:
            recommendations += "1. Acompanhamento clínico em 3-6 meses\n"
            recommendations += "2. Repetir citologia se persistência dos sintomas\n"
            recommendations += "3. Correlação com exames de imagem\n"
            recommendations += "4. Considerar biópsia se progressão dos achados\n"
        else:
            recommendations += "1. Seguimento de rotina conforme protocolo\n"
            recommendations += "2. Manter rastreamento preventivo regular\n"
            recommendations += "3. Orientações sobre fatores de risco\n"
        
        if quality_score < 70:
            recommendations += f"\n5. Repetir coleta para melhor qualidade da amostra\n"
            recommendations += "   (qualidade atual: {:.1f}/100)".format(quality_score)
        
        return recommendations

    def _calculate_confidence_score(self, total_cells, quality_score):
        """Calcula score de confiança da análise"""
        # Score baseado na qualidade da imagem e número de células
        quality_factor = quality_score / 100.0
        cell_count_factor = min(total_cells / 50.0, 1.0)  # Máximo em 50 células
        
        confidence = (quality_factor * 0.6) + (cell_count_factor * 0.4)
        return min(confidence, 1.0)

    def _generate_key_findings(self, total_cells, malignancy_pct, quality_score):
        """Gera lista de achados principais"""
        findings = [
            f"{total_cells} células analisadas",
            f"{malignancy_pct:.1f}% de células atípicas"
        ]
        
        if quality_score >= 80:
            findings.append("Excelente qualidade da amostra")
        elif quality_score >= 60:
            findings.append("Boa qualidade da amostra")
        else:
            findings.append("Qualidade da amostra limitada")
        
        if malignancy_pct > 30:
            findings.append("Atipias significativas detectadas")
        elif malignancy_pct > 10:
            findings.append("Atipias moderadas detectadas")
        else:
            findings.append("Morfologia dentro da normalidade")
        
        return findings

    def _generate_risk_assessment(self, malignancy_pct):
        """Gera avaliação de risco"""
        if malignancy_pct > 30:
            return "Alto risco - Investigação adicional urgente recomendada"
        elif malignancy_pct > 10:
            return "Risco moderado - Acompanhamento clínico recomendado"
        else:
            return "Baixo risco - Achados dentro da normalidade"

    def _generate_error_response(self):
        """Gera resposta de erro"""
        return {
            "medical_analysis": "Erro interno durante análise médica. Dados insuficientes para gerar relatório.",
            "diagnosis_summary": "Análise indisponível",
            "recommendations": "Consulte um especialista para avaliação manual da amostra.",
            "confidence_score": 0.0,
            "key_findings": ["Erro no processamento automático"],
            "risk_assessment": "Indeterminado - Análise manual necessária"
        }
