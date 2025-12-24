
import grpc
from server.grpc_server import CellposeService
from concurrent import futures
import protos.cellpose_pb2_grpc as cellpose_pb2_grpc

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cellpose_pb2_grpc.add_CellposeServiceServicer_to_server(CellposeService(), server)
    server.add_insecure_port("[::]:50051")
    print("[SERVER] Servidor gRPC rodando na porta 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()