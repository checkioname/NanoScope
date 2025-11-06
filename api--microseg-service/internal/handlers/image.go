package handlers

import (
	"bytes"
	"context"
	"encoding/base64"
	"encoding/json"
	"image/jpeg"
	"io"
	"log/slog"
	"net/http"

	pb "github.com/checkioname/api--microseg-service/internal/protos"
	"github.com/checkioname/api--microseg-service/internal/service"
	"github.com/go-chi/chi/v5"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type ImageHandler struct {
	R *chi.Mux
}

func (i *ImageHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	i.R.ServeHTTP(w, r)
}

// GetFullImageData retorna todos os dados do processamento Cellpose
func (i *ImageHandler) GetFullImageData(imageData []byte) (*pb.ImageResponse, error) {
	grpcServerAddr := "localhost:50051"

	// Configurar opções do cliente para mensagens grandes
	opts := []grpc.DialOption{
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithDefaultCallOptions(
			grpc.MaxCallRecvMsgSize(50*1024*1024), // 50MB
			grpc.MaxCallSendMsgSize(50*1024*1024), // 50MB
		),
	}

	conn, err := grpc.NewClient(grpcServerAddr, opts...)
	if err != nil {
		slog.Warn("Erro ao conectar ao servidor gRPC:", err)
		return nil, err
	}
	defer conn.Close()

	client := pb.NewCellposeServiceClient(conn)

	req := &pb.ImageRequest{
		ImageData: imageData,
	}

	// Chamar o serviço gRPC
	resp, err := client.ProcessImage(context.Background(), req)
	if err != nil {
		slog.Warn("Erro no processamento gRPC:", err)
		return nil, err
	}

	return resp, nil
}

// GetImageData mantém compatibilidade (método legado)
func (i *ImageHandler) GetImageData(imageData []byte) ([]int32, []*pb.Outline, error) {
	resp, err := i.GetFullImageData(imageData)
	if err != nil {
		return nil, nil, err
	}
	return resp.Masks, resp.Outlines, nil
}

func (i *ImageHandler) ProcessImageData() {

}

// ImageAnalysisResponse representa a resposta completa com análise
type ImageAnalysisResponse struct {
	ProcessedImage   string                     `json:"processedImage"`
	CellFeatures     []*pb.CellFeature         `json:"cellFeatures"`
	GlobalMetrics    *pb.GlobalMetrics         `json:"globalMetrics"`
	TotalCells       int32                     `json:"totalCells"`
	Outlines         []*pb.Outline             `json:"outlines"`
	MedicalAnalysis  *service.MeditronAnalysis `json:"medicalAnalysis,omitempty"`
}

func (i *ImageHandler) UploadImage(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseMultipartForm(32 << 20); err != nil {
		slog.Error("Erro no parsing da request", "error", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	files := r.MultipartForm.File["file"]
	if len(files) == 0 {
		http.Error(w, "Nenhum arquivo enviado", http.StatusBadRequest)
		return
	}

	img, err := files[0].Open()
	if err != nil {
		slog.Error("Erro ao abrir arquivo", "error", err)
		http.Error(w, "Erro ao processar arquivo", http.StatusInternalServerError)
		return
	}
	defer img.Close()

	imageBytes, err := io.ReadAll(img)
	if err != nil {
		slog.Error("Erro ao ler imagem", "error", err)
		http.Error(w, "Erro ao processar imagem", http.StatusInternalServerError)
		return
	}

	// 1. Processar com Cellpose
	cellposeResp, err := i.GetFullImageData(imageBytes)
	if err != nil {
		slog.Error("Erro no processamento Cellpose", "error", err)
		http.Error(w, "Erro no processamento de imagem", http.StatusInternalServerError)
		return
	}

	// 2. Renderizar imagem com máscaras
	imageSegmented, err := service.RenderImageWithMask(w, imageBytes, cellposeResp.Masks)
	if err != nil {
		slog.Error("Erro ao renderizar imagem", "error", err)
		http.Error(w, "Erro ao renderizar imagem com máscara", http.StatusInternalServerError)
		return
	}

	// 3. Converter imagem para base64
	var buf bytes.Buffer
	if err := jpeg.Encode(&buf, imageSegmented, nil); err != nil {
		slog.Error("Erro ao codificar imagem", "error", err)
		http.Error(w, "Erro ao processar imagem", http.StatusInternalServerError)
		return
	}
	imageBase64 := "data:image/jpeg;base64," + base64.StdEncoding.EncodeToString(buf.Bytes())

	// 4. Gerar análise médica com Meditron
	meditronClient := service.NewMeditronClient()
	medicalAnalysis, err := meditronClient.GenerateAnalysis(
		cellposeResp.CellFeatures,
		cellposeResp.GlobalMetrics,
		"tissue sample", // Contexto padrão
	)
	if err != nil {
		slog.Warn("Erro na análise Meditron, continuando sem análise médica", "error", err)
		medicalAnalysis = nil
	}

	// 5. Criar resposta JSON completa
	response := ImageAnalysisResponse{
		ProcessedImage:  imageBase64,
		CellFeatures:    cellposeResp.CellFeatures,
		GlobalMetrics:   cellposeResp.GlobalMetrics,
		TotalCells:      int32(len(cellposeResp.CellFeatures)),
		Outlines:        cellposeResp.Outlines,
		MedicalAnalysis: medicalAnalysis,
	}

	// 6. Enviar resposta JSON
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.WriteHeader(http.StatusOK)

	if err := json.NewEncoder(w).Encode(response); err != nil {
		slog.Error("Erro ao codificar JSON", "error", err)
		http.Error(w, "Erro interno do servidor", http.StatusInternalServerError)
		return
	}

	slog.Info("Processamento completo", 
		"total_cells", response.TotalCells,
		"has_medical_analysis", medicalAnalysis != nil)
}
