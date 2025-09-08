from cellpose import models
import numpy as np
import cv2

class CellposeProcessor:
    def __init__(self, model_type="cyto"):
        self.model = models.Cellpose(model_type=model_type)

    def process_image(self, image):
        try:
            if image is None:
                raise ValueError("Falha ao decodificar imagem. Verifique o formato dos bytes enviados.")

            original_height, original_width = image.shape[:2]

            # Normalização
            image = (image - image.min()) / (image.max() - image.min()) * 255
            image = image.astype(np.uint8)

            # Resize para 512x512
            image_resized = cv2.resize(image, (512, 512), interpolation=cv2.INTER_LINEAR)

            # Avaliação com Cellpose
            masks, flows, styles, diams = self.model.eval(image_resized, diameter=30, channels=[0, 0])

            if masks is not None:
                masks = cv2.resize(masks, (original_width, original_height), interpolation=cv2.INTER_NEAREST)
        

            # --- NOVO: Calcular o número de células segmentadas ---
            num_cells = 0
            if masks is not None:
                # Cellpose atribui um ID único (inteiro > 0) para cada célula.
                # Contar o número de IDs únicos (ignorando o 0, que é o background).
                num_cells = len(np.unique(masks[masks > 0]))
            print("Numero de celulas detectadas: ", num_cells)


            return masks, flows, styles, diams

        except Exception as e:
            print(f"Erro ao processar imagem: {e}")
            return None, None, None, None

