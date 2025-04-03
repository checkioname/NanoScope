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
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Processar a imagem com Cellpose
        processor = CellposeProcessor()
        masks, flows, styles, diams = processor.process_image(image)

        # Criar a resposta
        response = cellpose_pb2.ImageResponse(
            masks=masks.flatten().tolist(),
            diams=[float(d) for d in diams] if isinstance(diams, (list, np.ndarray)) else [float(diams)],
            styles=[float(s) for s in styles.flatten()],
            flows=[float(f) for f in np.array(flows).flatten()]
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
