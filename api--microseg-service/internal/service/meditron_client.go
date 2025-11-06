package service

import (
	"fmt"
	"log/slog"

	pb "github.com/checkioname/api--microseg-service/internal/protos"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

// MeditronAnalysis representa a resposta do serviço Meditron
type MeditronAnalysis struct {
	MedicalAnalysis   string   `json:"medical_analysis"`
	DiagnosisSummary  string   `json:"diagnosis_summary"`
	Recommendations   string   `json:"recommendations"`
	ConfidenceScore   float32  `json:"confidence_score"`
	KeyFindings       []string `json:"key_findings"`
	RiskAssessment    string   `json:"risk_assessment"`
}

// MeditronClient gerencia a comunicação com o serviço Meditron
type MeditronClient struct {
	serverAddr string
}

// NewMeditronClient cria um novo cliente para o serviço Meditron
func NewMeditronClient() *MeditronClient {
	return &MeditronClient{
		serverAddr: "localhost:50052", // Porta do serviço Meditron
	}
}

// GenerateAnalysis chama o serviço Meditron para gerar análise médica
func (m *MeditronClient) GenerateAnalysis(cellFeatures []*pb.CellFeature, globalMetrics *pb.GlobalMetrics, imageContext string) (*MeditronAnalysis, error) {
	// Por enquanto, vamos simular a chamada gRPC com uma análise baseada em regras
	// TODO: Implementar chamada gRPC real quando o protobuf estiver funcionando
	
	return m.generateRuleBasedAnalysis(cellFeatures, globalMetrics, imageContext)
}

// generateRuleBasedAnalysis gera análise baseada em regras (fallback)
func (m *MeditronClient) generateRuleBasedAnalysis(cellFeatures []*pb.CellFeature, globalMetrics *pb.GlobalMetrics, imageContext string) (*MeditronAnalysis, error) {
	if globalMetrics == nil {
		return nil, fmt.Errorf("globalMetrics não pode ser nil")
	}

	totalCells := globalMetrics.TotalCells
	malignantCells := globalMetrics.PotentiallyMalignantCells
	malignancyPct := globalMetrics.MalignancyPercentage
	qualityScore := globalMetrics.ImageQualityScore

	analysis := &MeditronAnalysis{}

	// Gerar análise médica baseada nos dados
	analysis.MedicalAnalysis = fmt.Sprintf(`
RELATÓRIO DE ANÁLISE CITOLÓGICA AUTOMATIZADA

DADOS QUANTITATIVOS:
- Total de células analisadas: %d
- Células com características atípicas: %d (%.1f%%)
- Densidade celular: %.2f células/mm²
- Tamanho médio das células: %.1f pixels
- Qualidade da imagem: %.1f/100

INTERPRETAÇÃO DOS ACHADOS:
%s

CARACTERÍSTICAS CELULARES:
%s`,
		totalCells,
		malignantCells,
		malignancyPct,
		globalMetrics.CellDensityPerMm2,
		globalMetrics.MeanCellSize,
		qualityScore,
		m.generateInterpretation(malignancyPct, qualityScore),
		m.generateCellularCharacteristics(cellFeatures))

	// Gerar resumo do diagnóstico
	analysis.DiagnosisSummary = fmt.Sprintf("Análise de %d células com %.1f%% de atipias detectadas", totalCells, malignancyPct)

	// Gerar recomendações
	analysis.Recommendations = m.generateRecommendations(malignancyPct, qualityScore)

	// Calcular score de confiança
	analysis.ConfidenceScore = m.calculateConfidenceScore(totalCells, qualityScore)

	// Gerar achados principais
	analysis.KeyFindings = []string{
		fmt.Sprintf("%d células analisadas", totalCells),
		fmt.Sprintf("%.1f%% de células atípicas", malignancyPct),
		fmt.Sprintf("Qualidade da amostra: %.1f/100", qualityScore),
	}

	// Avaliação de risco
	analysis.RiskAssessment = m.generateRiskAssessment(malignancyPct)

	slog.Info("Análise Meditron gerada", "confidence", analysis.ConfidenceScore, "risk", analysis.RiskAssessment)

	return analysis, nil
}

func (m *MeditronClient) generateInterpretation(malignancyPct, qualityScore float32) string {
	if malignancyPct > 30 {
		return `Presença significativa de células com características atípicas. Observam-se irregularidades morfológicas importantes que requerem atenção especializada. As alterações incluem variações no tamanho nuclear, modificações na razão núcleo/citoplasma e irregularidades na cromatina.`
	} else if malignancyPct > 10 {
		return `Presença moderada de células com características atípicas. As alterações morfológicas observadas estão dentro de um padrão que requer acompanhamento, mas não indicam necessariamente malignidade. Recomenda-se correlação clínica.`
	} else {
		return `As células analisadas apresentam morfologia predominantemente dentro dos padrões de normalidade. As características citológicas observadas são compatíveis com tecido benigno, sem evidências significativas de atipia.`
	}
}

func (m *MeditronClient) generateCellularCharacteristics(cellFeatures []*pb.CellFeature) string {
	if len(cellFeatures) == 0 {
		return "Nenhuma característica celular individual disponível para análise."
	}

	// Contar células suspeitas
	suspiciousCells := 0
	for _, cell := range cellFeatures {
		if cell.IsPotentiallyMalignant {
			suspiciousCells++
		}
	}

	if suspiciousCells == 0 {
		return "Todas as células analisadas apresentam características morfológicas normais."
	}

	result := fmt.Sprintf("Das %d células analisadas, %d apresentam características atípicas:\n", len(cellFeatures), suspiciousCells)
	
	// Mostrar detalhes das primeiras células suspeitas
	count := 0
	for _, cell := range cellFeatures {
		if cell.IsPotentiallyMalignant && count < 3 {
			result += fmt.Sprintf("- Célula %d: Área=%.1f, Circularidade=%.2f, Razão N/C=%.2f\n", 
				cell.CellId, cell.Area, cell.Circularity, cell.NucleusCytoplasmRatio)
			count++
		}
	}

	return result
}

func (m *MeditronClient) generateRecommendations(malignancyPct, qualityScore float32) string {
	recommendations := []string{}

	if malignancyPct > 30 {
		recommendations = append(recommendations, "Revisão urgente por patologista experiente")
		recommendations = append(recommendations, "Considerar biópsia adicional se clinicamente indicado")
		recommendations = append(recommendations, "Correlação com exames de imagem e dados clínicos")
	} else if malignancyPct > 10 {
		recommendations = append(recommendations, "Acompanhamento clínico regular")
		recommendations = append(recommendations, "Repetir exame em 6 meses se indicado")
		recommendations = append(recommendations, "Correlação com histórico clínico do paciente")
	} else {
		recommendations = append(recommendations, "Seguimento de rotina conforme protocolo institucional")
		recommendations = append(recommendations, "Manter acompanhamento preventivo regular")
	}

	if qualityScore < 70 {
		recommendations = append(recommendations, "Considerar repetir coleta para melhor qualidade da amostra")
	}

	result := "RECOMENDAÇÕES CLÍNICAS:\n"
	for i, rec := range recommendations {
		result += fmt.Sprintf("%d. %s\n", i+1, rec)
	}

	return result
}

func (m *MeditronClient) calculateConfidenceScore(totalCells int32, qualityScore float32) float32 {
	// Score baseado na qualidade da imagem e número de células
	qualityFactor := qualityScore / 100.0
	cellCountFactor := float32(totalCells) / 100.0
	if cellCountFactor > 1.0 {
		cellCountFactor = 1.0
	}

	confidence := (qualityFactor + cellCountFactor) / 2.0
	if confidence > 1.0 {
		confidence = 1.0
	}

	return confidence
}

func (m *MeditronClient) generateRiskAssessment(malignancyPct float32) string {
	if malignancyPct > 30 {
		return "Alto risco - Investigação adicional urgente recomendada"
	} else if malignancyPct > 10 {
		return "Risco moderado - Acompanhamento clínico recomendado"
	} else {
		return "Baixo risco - Achados dentro da normalidade"
	}
}

// TODO: Implementar chamada gRPC real
func (m *MeditronClient) callMeditronGRPC(cellFeatures []*pb.CellFeature, globalMetrics *pb.GlobalMetrics, imageContext string) (*MeditronAnalysis, error) {
	conn, err := grpc.NewClient(m.serverAddr, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return nil, fmt.Errorf("erro ao conectar ao Meditron: %w", err)
	}
	defer conn.Close()

	// TODO: Usar o cliente gRPC gerado quando o protobuf estiver funcionando
	// client := meditron_pb.NewMeditronServiceClient(conn)
	
	slog.Warn("Chamada gRPC para Meditron não implementada, usando análise baseada em regras")
	return m.generateRuleBasedAnalysis(cellFeatures, globalMetrics, imageContext)
}

