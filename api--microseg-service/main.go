package main

import (
	"io"
	"log/slog"
	"net/http"

	"github.com/go-chi/chi/v5"
)




type imageHandler struct {
  R *chi.Mux
}

func (i *imageHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
  i.R.ServeHTTP(w, r)
}

func (i *imageHandler) GetImageData(buf io.Reader) []byte{
  modelurl := "localhost:8003"
  resp, err := http.Post(modelurl, "image/png", buf)
  
  if err != nil {
    slog.Error("could not reach the api")
  }

  defer resp.Body.Close()
  body, _ := io.ReadAll(resp.Body)

  return body
}


func main() {
  
  // Pegar dados da imagem

  //aplicar regra de negocio

  //devolver para o usuario
}




