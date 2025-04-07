package handlers

import (
	"context"
	"fmt"
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

func (i *ImageHandler) GetImageData(imageData []byte) ([]int32, error) {
	grpcServerAddr := "localhost:50051"

	conn, err := grpc.Dial(grpcServerAddr, grpc.WithTransportCredentials(insecure.NewCredentials()))
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

	return resp.Masks, nil
}

func (i *ImageHandler) ProcessImageData() {

}

func (i *ImageHandler) UploadImage(w http.ResponseWriter, r *http.Request){
	fmt.Println("RECEBI UMA REQUEEEEEST")
	if err := r.ParseMultipartForm(32); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	files := r.MultipartForm.File["file"]
	img, _ := files[0].Open()
	
	imageBytes, _ := io.ReadAll(img)
	masks, _ := i.GetImageData(imageBytes)

	// Exibir resultado no console
	imageSegmented, err := service.RenderImageWithMask(w, imageBytes, masks)
	
	if err != nil {
		http.Error(w, "Erro ao renderizar imagem com máscara", http.StatusInternalServerError)
	}
	// Enviar como resposta
	w.Header().Set("Content-Type", "image/jpeg")
	w.WriteHeader(http.StatusOK)
	jpeg.Encode(w, imageSegmented, nil)
}
