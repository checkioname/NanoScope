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
    
        
        outline_mask = np.zeros((original_height, original_width), dtype=np.uint32)
        if outlines is not None:
            temp_mask = np.zeros((original_height, original_width), dtype=np.uint8)
            cv2.drawContours(temp_mask, outlines, -1, 255, 1)
            
            outline_mask = temp_mask.astype(np.int32)

        flattened_mask = outline_mask.flatten().tolist()
        
        # Criar a resposta (por enquanto enviar somente a mascara)
        response = cellpose_pb2.ImageResponse(
            masks=flattened_mask
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
