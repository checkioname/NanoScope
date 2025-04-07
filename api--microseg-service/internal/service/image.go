package service

import (
	"bytes"
	"fmt"
	"image"
	"image/color"
	"image/draw"
	"net/http"
)



func RenderImageWithMask(w http.ResponseWriter, original []byte, masks []int32) (*image.RGBA, error) {
	img, _, err := image.Decode(bytes.NewReader(original))
	if err != nil {
		return nil, err
	}

	bounds := img.Bounds()
	width, height := bounds.Dx(), bounds.Dy()

	if len(masks) != width*height {
		return nil, fmt.Errorf("máscara tem tamanho incompatível com a imagem")
	}

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


