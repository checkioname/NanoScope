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
        

        flattened_mask = masks.flatten().tolist() if masks is not None else [0]
        flattened_diams = [0] # [float(d) for d in diams] if isinstance(diams, (list, np.ndarray)) else [float(diams)] if diams is not None else [0],
        flattened_styles = [0] # [float(s) for s in styles.flatten()] if styles is not None else [0],
        flattened_flows = [0] # [float(f) for f in np.array(flows).flatten()] if flows is not None else [0]
        
        outline_mask_bytes = b''
        if outlines is not None:
            outline_mask = np.zeros((original_height, original_width), dtype=np.uint8)
            cv2.drawContours(outline_mask, outlines, -1, 255, 1)
            
            _, encoded_mask = cv2.imencode('.png', outline_mask)
            outline_mask_bytes = encoded_mask.tobytes()

        outlines = get_outlines(outlines)
    
        print(flattened_diams)
        print(flattened_styles)
        print(flattened_flows)
        
        # Criar a resposta
        response = cellpose_pb2.ImageResponse(
            outlines=outlines,
            masks=outline_mask_bytes,
            diams=flattened_diams,
            styles=flattened_styles,
            rows=flattened_flows
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
