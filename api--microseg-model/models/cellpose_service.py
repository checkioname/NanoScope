from cellpose import models, utils
import numpy as np
import cv2
import numpy as np
from scipy import ndimage
from skimage import measure, morphology

class CellposeProcessor:
    def __init__(self, model_type="cyto"):
        self.model = models.Cellpose(model_type=model_type)

    def process_image(self, image, original_width, original_height):
        try:
            if image is None:
                raise ValueError("Falha ao decodificar imagem. Verifique o formato dos bytes enviados.")

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
            outlines = utils.outlines_list(masks)

            return masks, outlines, flows, styles, diams

        except Exception as e:
            print(f"Erro ao processar imagem: {e}")
            return None, None, None, None

    def calculate_cell_features(self, image, masks):
        """Calcula características detalhadas de cada célula"""
        features = []
        
        if masks is None:
            return features
            
        # Converter imagem para escala de cinza se necessário
        if len(image.shape) == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image
            
        unique_cells = np.unique(masks[masks > 0])
        
        for cell_id in unique_cells:
            cell_mask = (masks == cell_id)
            
            # Propriedades regionais
            props = measure.regionprops(cell_mask.astype(int), intensity_image=gray_image)[0]
            
            # Características morfológicas
            area = props.area
            perimeter = props.perimeter
            circularity = 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0
            eccentricity = props.eccentricity
            solidity = props.solidity
            
            # Características de intensidade (importante para células cancerígenas)
            mean_intensity = props.mean_intensity
            max_intensity = props.max_intensity
            min_intensity = props.min_intensity
            intensity_std = np.std(gray_image[cell_mask])
            
            # Características de textura
            cell_pixels = gray_image[cell_mask]
            texture_contrast = np.std(cell_pixels)
            
            # Razão núcleo/citoplasma (aproximação)
            # Células cancerígenas geralmente têm núcleos maiores
            nucleus_area = np.sum(cell_pixels < np.percentile(cell_pixels, 30))  # pixels mais escuros
            nucleus_cytoplasm_ratio = nucleus_area / area if area > 0 else 0
            
            features.append({
                'cell_id': int(cell_id),
                'area': float(area),
                'perimeter': float(perimeter),
                'circularity': float(circularity),
                'eccentricity': float(eccentricity),
                'solidity': float(solidity),
                'mean_intensity': float(mean_intensity),
                'max_intensity': float(max_intensity),
                'min_intensity': float(min_intensity),
                'intensity_std': float(intensity_std),
                'texture_contrast': float(texture_contrast),
                'nucleus_cytoplasm_ratio': float(nucleus_cytoplasm_ratio),
                'is_potentially_malignant': self.assess_malignancy_risk(
                    circularity, nucleus_cytoplasm_ratio, intensity_std, area
                )
            })
            
        return features
    
    def assess_malignancy_risk(self, circularity, nc_ratio, intensity_std, area):
        """Avaliação básica de risco de malignidade baseada em características morfológicas"""
        risk_score = 0
        
        # Células cancerígenas tendem a ser menos circulares
        if circularity < 0.7:
            risk_score += 1
            
        # Núcleo grande em relação ao citoplasma
        if nc_ratio > 0.3:
            risk_score += 1
            
        # Alta variabilidade de intensidade (textura irregular)
        if intensity_std > 30:
            risk_score += 1
            
        # Células muito grandes ou muito pequenas podem ser suspeitas
        if area > 1000 or area < 50:
            risk_score += 1
            
        return risk_score >= 2  # 2 ou mais critérios = potencialmente maligna
    
    def calculate_global_metrics(self, image, masks, cell_features):
        """Calcula métricas globais da imagem"""
        try:
            if masks is None or len(cell_features) == 0:
                return {
                    'total_cells': 0,
                    'potentially_malignant_cells': 0,
                    'malignancy_percentage': 0.0,
                    'cell_density_per_mm2': 0.0,
                    'mean_cell_size': 0.0,
                    'cell_size_variability': 0.0,
                    'mean_cell_intensity': 0.0,
                    'intensity_variability': 0.0,
                    'image_quality_score': 0.0
                }
                
            total_cells = len(cell_features)
            potentially_malignant = sum(1 for f in cell_features if f['is_potentially_malignant'])
            
            # Densidade celular
            image_area = image.shape[0] * image.shape[1]
            cell_density = total_cells / image_area * 1000000  # células por mm² (assumindo escala)
            
            # Estatísticas de tamanho
            areas = [f['area'] for f in cell_features]
            mean_cell_size = np.mean(areas) if areas else 0.0
            size_variability = (np.std(areas) / mean_cell_size) if mean_cell_size > 0 else 0.0
            
            # Distribuição de intensidades
            intensities = [f['mean_intensity'] for f in cell_features]
            mean_intensity = np.mean(intensities) if intensities else 0.0
            intensity_variability = np.std(intensities) if intensities else 0.0
            
            return {
                'total_cells': total_cells,
                'potentially_malignant_cells': potentially_malignant,
                'malignancy_percentage': (potentially_malignant / total_cells * 100) if total_cells > 0 else 0.0,
                'cell_density_per_mm2': float(cell_density),
                'mean_cell_size': float(mean_cell_size),
                'cell_size_variability': float(size_variability),
                'mean_cell_intensity': float(mean_intensity),
                'intensity_variability': float(intensity_variability),
                'image_quality_score': self.assess_image_quality(image)
            }
        except Exception as e:
            print(f"Erro ao calcular métricas globais: {e}")
            return {
                'total_cells': 0,
                'potentially_malignant_cells': 0,
                'malignancy_percentage': 0.0,
                'cell_density_per_mm2': 0.0,
                'mean_cell_size': 0.0,
                'cell_size_variability': 0.0,
                'mean_cell_intensity': 0.0,
                'intensity_variability': 0.0,
                'image_quality_score': 0.0
            }
    
    def assess_image_quality(self, image):
        """Avalia a qualidade da imagem para análise"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        # Nitidez (Laplacian variance)
        sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Contraste
        contrast = gray.std()
        
        # Score normalizado (0-100)
        quality_score = min(100, (sharpness / 100 + contrast / 50) * 50)
        
        return float(quality_score)

