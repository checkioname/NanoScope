from cellpose import models
import numpy as np
import cv2

class CellposeProcessor:
    def __init__(self, model_type="cyto"):
        self.model = models.Cellpose(model_type=model_type)

    def process_image(self, image):
        # Normalização
        image = (image - image.min()) / (image.max() - image.min()) * 255
        image = image.astype(np.uint8)

        # Resize
        image_resized = cv2.resize(image, (512, 512), interpolation=cv2.INTER_LINEAR)

        # Avaliação com Cellpose
        masks, flows, styles, diams = self.model.eval(image_resized, diameter=30, channels=[0, 0])

        return masks, flows, styles, diams

