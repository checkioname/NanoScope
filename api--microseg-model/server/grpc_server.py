import grpc
from concurrent import futures
import numpy as np
import cv2
import protos.cellpose_pb2 as cellpose_pb2
import protos.cellpose_pb2_grpc as cellpose_pb2_grpc
from models.cellpose_service import CellposeProcessor

class CellposeService(cellpose_pb2_grpc.CellposeServiceServicer):
    def ProcessImage(self, request, context):
        print("[SERVER] Recebendo imagem para processamento...")

        # Convertendo os bytes da imagem para um array numpy
        nparr = np.frombuffer(request.image_data, np.uint8)
        print(nparr)
        print("NUMPY ARRAY DA IMAGEM RECEBIDA")
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Processar a imagem com Cellpose
        processor = CellposeProcessor()
        masks, flows, styles, diams = processor.process_image(image)
        

        print("flows:", type(flows), len(flows))
        for i, f in enumerate(flows):
            print(f"[{i}] shape:", np.shape(f))

        flattened_mask = masks.flatten().tolist() if masks is not None else [0]
        flattened_diams = [0] # [float(d) for d in diams] if isinstance(diams, (list, np.ndarray)) else [float(diams)] if diams is not None else [0],
        flattened_styles = [0] # [float(s) for s in styles.flatten()] if styles is not None else [0],
        flattened_flows = [0] # [float(f) for f in np.array(flows).flatten()] if flows is not None else [0]
        print(flattened_mask)
        print(flattened_diams)
        print(flattened_styles)
        print(flattened_flows)
        # Criar a resposta
        response = cellpose_pb2.ImageResponse(
            masks=flattened_mask,
            diams=flattened_diams,
            styles=flattened_styles,
            rows=flattened_flows
        )

        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cellpose_pb2_grpc.add_CellposeServiceServicer_to_server(CellposeService(), server)
    server.add_insecure_port("[::]:50051")
    print("[SERVER] Servidor gRPC rodando na porta 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
