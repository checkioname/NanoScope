package handlers

import (
	"fmt"
	"io"
	"log/slog"
	"net/http"

	"github.com/go-chi/chi/v5"
)


type ImageHandler struct {
  R *chi.Mux
}

func (i *ImageHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
  i.R.ServeHTTP(w, r)
}

func (i *ImageHandler) GetImageData(buf io.Reader) []byte{
  modelurl := "localhost:8003"
  resp, err := http.Post(modelurl, "image/png", buf)
  
  if err != nil {
    slog.Error("could not reach the api")
  }

  defer resp.Body.Close()
  body, _ := io.ReadAll(resp.Body)

  return body
}


func (i *ImageHandler) ProcessImageData() {

}



func (i *ImageHandler) UploadImage(w http.ResponseWriter, r *http.Request) {
  fmt.Println("RECEBI UMA REQUEEEEEST")
  if err := r.ParseMultipartForm(32); err != nil {
    http.Error(w, err.Error(), http.StatusInternalServerError)
    return
  }

  images := r.MultipartForm.File["file"]
  
  fmt.Println(images)
}
