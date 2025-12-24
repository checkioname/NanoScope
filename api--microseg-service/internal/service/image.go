package service

import (
	"bytes"
	"image"
	"image/color"
	"image/draw"
	"net/http"

	_ "image/gif"  // Para imagens GIF
	_ "image/jpeg" // Para imagens JPEG
	_ "image/png"  // Para imagens PNG
)

func RenderImageWithMask(w http.ResponseWriter, original []byte, masks []int32) (*image.RGBA, error) {
	img, _, err := image.Decode(bytes.NewReader(original))
	if err != nil {
		return nil, err
	}

	bounds := img.Bounds()
	width, height := bounds.Dx(), bounds.Dy()

	// if len(masks) != width*height {
	// 	return nil, fmt.Errorf("máscara tem tamanho incompatível com a imagem")
	// }

	// Criar overlay com a máscara
	mask := image.NewRGBA(bounds)
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			i := y*width + x
			if masks[i] != 0 {
				// Define cor da máscara (ex: vermelho transparente)
				mask.Set(x, y, color.RGBA{255, 0, 0, 100})
			}
		}
	}

	// Compor imagem final
	final := image.NewRGBA(bounds)
	draw.Draw(final, bounds, img, image.Point{}, draw.Src)
	draw.Draw(final, bounds, mask, image.Point{}, draw.Over)

	return final, err
}

// func RenderImageWithOutlines(originalImageBytes []byte, outlineMaskData []int32) (*image.RGBA, error) {
// 	// 1. Decodificar a imagem original
// 	img, _, err := image.Decode(bytes.NewReader(originalImageBytes))
// 	if err != nil {
// 		return nil, fmt.Errorf("falha ao decodificar a imagem original: %w", err)
// 	}

// 	// 2. Decodificar a máscara de contorno PNG
// 	outlineMask, err := image.Decode(bytes.NewReader((bytes)(outlineMaskData))
// 	if err != nil {
// 		return nil, fmt.Errorf("falha ao decodificar a máscara de contorno: %w", err)
// 	}

// 	bounds := img.Bounds()
// 	width, height := bounds.Dx(), bounds.Dy()

// 	// 3. Criar a imagem final, copiando a original
// 	finalImage := image.NewRGBA(bounds)
// 	draw.Draw(finalImage, bounds, img, image.Point{}, draw.Src)

// 	// 4. Definir a cor para os contornos (verde como na imagem fornecida)
// 	outlineColor := color.RGBA{R: 0, G: 255, B: 0, A: 255}

// 	// 5. Percorrer a máscara de contorno e colorir os pixels do contorno
// 	for y := 0; y < height; y++ {
// 		for x := 0; x < width; x++ {
// 			// A máscara de contorno é em escala de cinza, verificamos o valor R
// 			r, _, _, _ := outlineMask.At(x, y).RGBA()

// 			// Se o pixel na máscara não for preto, ele faz parte de um contorno.
// 			// 65535 é o valor máximo (branco) no formato RGBA do Go.
// 			// Qualquer valor > 0 significa um pixel desenhado.
// 			if r > 0 {
// 				finalImage.Set(x, y, outlineColor)
// 			}
// 		}
// 	}

// 	return finalImage, nil
// }
