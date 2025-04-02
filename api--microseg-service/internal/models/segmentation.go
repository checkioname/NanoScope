package models

type SegmentationResponse struct {
	masks  [][]int
	flows  []int
	styles []int
	diams  float32
}
