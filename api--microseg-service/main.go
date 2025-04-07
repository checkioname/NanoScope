package main

import (
	"errors"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"

	"github.com/checkioname/api--microseg-service/internal/handlers"
)






func main() {
  h := handlers.ImageHandler{}

  handler := handlers.NewHandler(&h)
  // fmt.Println(handler)

  go func() {
    if err := http.ListenAndServe(":3000", handler); err != nil {
      if !errors.Is(err, http.ErrServerClosed) {
        log.Fatal("Couldn't keep up the server alive", err)
        panic(err)
      }
    }
  }()

  fmt.Println("Listening on port 3000...")
  quit := make(chan os.Signal, 1)
  signal.Notify(quit, os.Interrupt)
  <-quit

  // Pegar dados da imagem
  // mask := handler.GetImageMask()

  //aplicar regra de negocio

  //devolver para o usuario
}




