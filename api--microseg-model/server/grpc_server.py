import grpc
import cv2
import numpy as np
from concurrent import futures

import protos.cellpose_pb2 as cellpose_pb2
import protos.cellpose_pb2_grpc as cellpose_pb2_grpc

from models.cellpose_service import CellposeProcessor

class CellposeService(cellpose_pb2_grpc.CellposeServiceServicer):
    def ProcessImage(self, request, context):
        print("[SERVER] Recebendo imagem para processamento...")

        # Convertendo os bytes da imagem para um array numpy
        nparr = np.frombuffer(request.image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        original_height, original_width = image.shape[:2]
        
        # Processar a imagem com Cellpose
        processor = CellposeProcessor()
        masks, outlines, flows, styles, diams = processor.process_image(image, original_width, original_height)
        
        # Calcular características das células
        cell_features = processor.calculate_cell_features(image, masks)
        global_metrics = processor.calculate_global_metrics(image, masks, cell_features)
        
        # Criar máscara de contornos
        outline_mask = np.zeros((original_height, original_width), dtype=np.int32)
        if outlines is not None:
            temp_mask = np.zeros((original_height, original_width), dtype=np.uint8)
            cv2.drawContours(temp_mask, outlines, -1, 1, 1)
            outline_mask = temp_mask.astype(np.int32)
        
        flattened_mask = outline_mask.flatten().tolist()
        outlines_proto = get_outlines(outlines)
        
        # Converter características das células para protobuf
        cell_features_proto = []
        for feature in cell_features:
            cell_feature_proto = cellpose_pb2.CellFeature(
                cell_id=feature['cell_id'],
                area=feature['area'],
                perimeter=feature['perimeter'],
                circularity=feature['circularity'],
                eccentricity=feature['eccentricity'],
                solidity=feature['solidity'],
                mean_intensity=feature['mean_intensity'],
                max_intensity=feature['max_intensity'],
                min_intensity=feature['min_intensity'],
                intensity_std=feature['intensity_std'],
                texture_contrast=feature['texture_contrast'],
                nucleus_cytoplasm_ratio=feature['nucleus_cytoplasm_ratio'],
                is_potentially_malignant=feature['is_potentially_malignant']
            )
            cell_features_proto.append(cell_feature_proto)
        
        # Converter métricas globais para protobuf
        global_metrics_proto = cellpose_pb2.GlobalMetrics(
            total_cells=global_metrics['total_cells'],
            potentially_malignant_cells=global_metrics['potentially_malignant_cells'],
            malignancy_percentage=global_metrics['malignancy_percentage'],
            cell_density_per_mm2=global_metrics['cell_density_per_mm2'],
            mean_cell_size=global_metrics['mean_cell_size'],
            cell_size_variability=global_metrics['cell_size_variability'],
            mean_cell_intensity=global_metrics['mean_cell_intensity'],
            intensity_variability=global_metrics['intensity_variability'],
            image_quality_score=global_metrics['image_quality_score']
        )
        
        # Criar a resposta
        response = cellpose_pb2.ImageResponse(
            outlines=outlines_proto,
            masks=flattened_mask,
            diams=[float(d) for d in diams] if isinstance(diams, (list, np.ndarray)) else [float(diams)] if diams is not None else [0.0],
            styles=[float(s) for s in styles.flatten()] if styles is not None else [0.0],
            rows=[float(f) for f in np.array(flows).flatten()] if flows is not None else [0.0],
            cell_features=cell_features_proto,
            global_metrics=global_metrics_proto
        )

        return response

def get_outlines(outlines_np):
    outlines_proto = []
    if outlines_np is not None:
        for outline_array in outlines_np:
            points_proto = []
            for point in outline_array:
                p = cellpose_pb2.Point(y=int(point[0]), x=int(point[1]))
                points_proto.append(p)
            
            outline_proto = cellpose_pb2.Outline(points=points_proto)
            outlines_proto.append(outline_proto)

    return outlines_proto

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cellpose_pb2_grpc.add_CellposeServiceServicer_to_server(CellposeService(), server)
    server.add_insecure_port("[::]:50051")
    print("[SERVER] Servidor gRPC rodando na porta 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
