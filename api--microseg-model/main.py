from cellpose import models
import numpy as np
import cv2


filepath = "/home/king/Downloads/microscopic.png"
image = cv2.imread(filepath)

# normalizacao
image = (image - image.min()) / (image.max() - image.min()) * 255
image = image.astype(np.uint8)

# resize da imagem
image_resized = cv2.resize(image, (512,512), interpolation=cv2.INTER_LINEAR)


model = models.Cellpose(model_type="cyto")

masks, flows, styles, diams = model.eval(image_resized, diameter=30, channels=[0,0])


print(np.sum(masks.tolist()))
print(masks.tolist())


overlay = image_resized.copy()

# Gerar contornos das máscaras
contours, _ = cv2.findContours(masks.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Desenhar os contornos na imagem original
cv2.drawContours(overlay, contours, -1, (0, 255, 0), 2)  # Verde para os contornos

# Combinar imagem original e máscara
alpha = 0.5  # Ajuste a transparência da máscara
final_image = cv2.addWeighted(overlay, alpha, image_resized, 1 - alpha, 0)

# Caminho da imagem de saída
output_path = "microscopic_segmented.png"
cv2.imwrite(output_path, final_image)
