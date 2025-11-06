package service

import "github.com/checkioname/api--microseg-service/internal/models"

const (
	prompt = "based on this data about biopsis cell, indicate valueable information considering the follwoing pattern: "
)

func preparePromt(segmentationResponse *models.SegmentationResponse) string {
	return prompt + segmentationResponse.GetValues()
}
