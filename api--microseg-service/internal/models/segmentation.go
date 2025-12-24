package models

type SegmentationResponse struct {
	masks  [][]int
	flows  []int
	styles []int
	diams  float32
}

func (sr *SegmentationResponse) GetValues() string {
	response := ""

// 	for i range := sr.masks[]
// 		for j := range masks[i][] {
// 			response = response + string(j)
// 		}
// 	}

	return response
}
