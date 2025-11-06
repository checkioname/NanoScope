import grpc
import cv2
import numpy as np
from concurrent import futures

import protos.cellpose_pb2 as cellpose_pb2
import protos.cellpose_pb2_grpc as cellpose_pb2_grpc

from models.cellpose_service import CellposeProcessor

class CellposeService(cellpose_pb2_grpc.CellposeServiceServicer):
    def ProcessImage(self, request, context):
        try:
            print("[SERVER] Recebendo imagem para processamento...")

            # Convertendo os bytes da imagem para um array numpy
            nparr = np.frombuffer(request.image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if image is None:
                raise ValueError("Falha ao decodificar a imagem")

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
            
            # Processar diams de forma segura
            processed_diams = []
            if diams is not None:
                if isinstance(diams, (list, tuple)):
                    processed_diams = [float(d) for d in diams if np.isfinite(d)]
                elif isinstance(diams, np.ndarray):
                    diams_flat = diams.flatten()
                    processed_diams = [float(d) for d in diams_flat if np.isfinite(d)]
                elif np.isscalar(diams) and np.isfinite(diams):
                    processed_diams = [float(diams)]
            
            if not processed_diams:
                processed_diams = [0.0]
            
            # Processar styles de forma segura
            processed_styles = []
            if styles is not None:
                if isinstance(styles, np.ndarray):
                    styles_flat = styles.flatten()
                    processed_styles = [float(s) for s in styles_flat if np.isfinite(s)]
                elif isinstance(styles, (list, tuple)):
                    processed_styles = [float(s) for s in styles if np.isfinite(s)]
            
            if not processed_styles:
                processed_styles = [0.0]
            
            # Processar flows de forma segura
            processed_flows = []
            if flows is not None:
                try:
                    if isinstance(flows, (list, tuple)):
                        # flows pode ser uma lista de arrays
                        for flow_item in flows:
                            if isinstance(flow_item, np.ndarray):
                                flow_flat = flow_item.flatten()
                                processed_flows.extend([float(f) for f in flow_flat if np.isfinite(f)])
                            elif np.isscalar(flow_item) and np.isfinite(flow_item):
                                processed_flows.append(float(flow_item))
                    elif isinstance(flows, np.ndarray):
                        flows_flat = flows.flatten()
                        processed_flows = [float(f) for f in flows_flat if np.isfinite(f)]
                except Exception as e:
                    print(f"Erro ao processar flows: {e}")
                    processed_flows = [0.0]
            
            if not processed_flows:
                processed_flows = [0.0]
            
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
                total_cells=global_metrics.get('total_cells', 0),
                potentially_malignant_cells=global_metrics.get('potentially_malignant_cells', 0),
                malignancy_percentage=global_metrics.get('malignancy_percentage', 0.0),
                cell_density_per_mm2=global_metrics.get('cell_density_per_mm2', 0.0),
                mean_cell_size=global_metrics.get('mean_cell_size', 0.0),
                cell_size_variability=global_metrics.get('cell_size_variability', 0.0),
                mean_cell_intensity=global_metrics.get('mean_cell_intensity', 0.0),
                intensity_variability=global_metrics.get('intensity_variability', 0.0),
                image_quality_score=global_metrics.get('image_quality_score', 0.0)
            )
            
            # Criar a resposta
            response = cellpose_pb2.ImageResponse(
                outlines=outlines_proto,
                masks=flattened_mask,
                diams=processed_diams,
                styles=processed_styles,
                rows=processed_flows,
                cell_features=cell_features_proto,
                global_metrics=global_metrics_proto
            )

            print(f"[SERVER] Processamento concluído. Células detectadas: {len(cell_features)}")
            return response
            
        except Exception as e:
            print(f"[SERVER] Erro durante processamento: {e}")
            import traceback
            traceback.print_exc()
            
            # Retornar resposta vazia em caso de erro
            return cellpose_pb2.ImageResponse(
                outlines=[],
                masks=[],
                diams=[0.0],
                styles=[0.0],
                rows=[0.0],
                cell_features=[],
                global_metrics=cellpose_pb2.GlobalMetrics()
            )

def get_outlines(outlines_np):
    outlines_proto = []
    if outlines_np is not None:
        try:
            for outline_array in outlines_np:
                points_proto = []
                if isinstance(outline_array, np.ndarray) and len(outline_array) > 0:
                    for point in outline_array:
                        if len(point) >= 2:
                            p = cellpose_pb2.Point(y=int(point[0]), x=int(point[1]))
                            points_proto.append(p)
                
                if points_proto:  # Só adicionar se tiver pontos válidos
                    outline_proto = cellpose_pb2.Outline(points=points_proto)
                    outlines_proto.append(outline_proto)
        except Exception as e:
            print(f"Erro ao processar outlines: {e}")
    
    return outlines_proto

def serve():
    # Configurar opções do servidor para mensagens grandes
    options = [
        ('grpc.max_send_message_length', 50 * 1024 * 1024),  # 50MB
        ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 50MB
        ('grpc.max_message_length', 50 * 1024 * 1024),  # 50MB
    ]
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=options)
    cellpose_pb2_grpc.add_CellposeServiceServicer_to_server(CellposeService(), server)
    server.add_insecure_port("[::]:50051")
    print("[CELLPOSE SERVER] Servidor gRPC rodando na porta 50051...")
    print("[CELLPOSE SERVER] Configurado para mensagens até 50MB")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
