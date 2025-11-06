import grpc
from concurrent import futures
import sys
import os

# Adicionar o diretório pai ao path para imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    import protos.meditron_pb2 as meditron_pb2
    import protos.meditron_pb2_grpc as meditron_pb2_grpc
    print("[MEDITRON SERVER] Protobuf importado com sucesso")
except ImportError as e:
    print(f"[MEDITRON SERVER] Erro na importação protobuf: {e}")
    raise

# Tentar diferentes analisadores em ordem de preferência
try:
    from model.lightweight_analyzer import LightweightMedicalAnalyzer
    # Você pode escolher o modelo aqui:
    # "openai" - OpenAI GPT (requer OPENAI_API_KEY)
    # "ollama" - Ollama local (requer Ollama instalado)
    # "huggingface" - Modelo pequeno do HuggingFace
    # "simple" - Análise baseada em regras
    
    MODEL_TYPE = "simple"  # Mude aqui para usar outros modelos
    AnalyzerClass = lambda: LightweightMedicalAnalyzer(model_type=MODEL_TYPE)
    print(f"[MEDITRON SERVER] Usando LightweightMedicalAnalyzer com modelo: {MODEL_TYPE}")
except ImportError as e:
    print(f"[MEDITRON SERVER] LightweightAnalyzer não disponível ({e}), usando SimpleMedicalAnalyzer")
    from model.simple_analyzer import SimpleMedicalAnalyzer
    AnalyzerClass = SimpleMedicalAnalyzer

class MeditronService(meditron_pb2_grpc.MeditronServiceServicer):
    def __init__(self):
        print("[MEDITRON SERVER] Inicializando serviço...")
        self.analyzer = AnalyzerClass()
        print("[MEDITRON SERVER] Serviço inicializado com sucesso!")
    
    def GenerateAnalysis(self, request, context):
        try:
            print("[MEDITRON SERVER] Recebendo solicitação de análise...")
            
            # Converter dados do protobuf para dicionários Python
            cell_features = []
            for cell in request.cell_features:
                cell_features.append({
                    'cell_id': cell.cell_id,
                    'area': cell.area,
                    'perimeter': cell.perimeter,
                    'circularity': cell.circularity,
                    'eccentricity': cell.eccentricity,
                    'solidity': cell.solidity,
                    'mean_intensity': cell.mean_intensity,
                    'max_intensity': cell.max_intensity,
                    'min_intensity': cell.min_intensity,
                    'intensity_std': cell.intensity_std,
                    'texture_contrast': cell.texture_contrast,
                    'nucleus_cytoplasm_ratio': cell.nucleus_cytoplasm_ratio,
                    'is_potentially_malignant': cell.is_potentially_malignant
                })
            
            global_metrics = {
                'total_cells': request.global_metrics.total_cells,
                'potentially_malignant_cells': request.global_metrics.potentially_malignant_cells,
                'malignancy_percentage': request.global_metrics.malignancy_percentage,
                'cell_density_per_mm2': request.global_metrics.cell_density_per_mm2,
                'mean_cell_size': request.global_metrics.mean_cell_size,
                'cell_size_variability': request.global_metrics.cell_size_variability,
                'mean_cell_intensity': request.global_metrics.mean_cell_intensity,
                'intensity_variability': request.global_metrics.intensity_variability,
                'image_quality_score': request.global_metrics.image_quality_score
            }
            
            # Gerar análise médica
            analysis_result = self.analyzer.generate_medical_analysis(
                cell_features=cell_features,
                global_metrics=global_metrics,
                image_context=request.image_context or "tissue sample"
            )
            
            # Criar resposta
            response = meditron_pb2.AnalysisResponse(
                medical_analysis=analysis_result['medical_analysis'],
                diagnosis_summary=analysis_result['diagnosis_summary'],
                recommendations=analysis_result['recommendations'],
                confidence_score=analysis_result['confidence_score'],
                key_findings=analysis_result['key_findings'],
                risk_assessment=analysis_result['risk_assessment']
            )
            
            print(f"[MEDITRON SERVER] Análise gerada com sucesso. Confiança: {analysis_result['confidence_score']:.2f}")
            return response
            
        except Exception as e:
            print(f"[MEDITRON SERVER] Erro durante análise: {e}")
            import traceback
            traceback.print_exc()
            
            # Retornar resposta de erro
            return meditron_pb2.AnalysisResponse(
                medical_analysis="Erro interno do servidor durante análise",
                diagnosis_summary="Análise indisponível",
                recommendations="Consulte um especialista",
                confidence_score=0.0,
                key_findings=["Erro no processamento"],
                risk_assessment="Indeterminado"
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    meditron_pb2_grpc.add_MeditronServiceServicer_to_server(MeditronService(), server)
    
    listen_addr = '[::]:50052'  # Porta diferente do Cellpose (50051)
    server.add_insecure_port(listen_addr)
    
    print(f"[MEDITRON SERVER] Iniciando servidor na porta 50052...")
    server.start()
    print(f"[MEDITRON SERVER] Servidor rodando em {listen_addr}")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("[MEDITRON SERVER] Parando servidor...")
        server.stop(0)

if __name__ == '__main__':
    serve()

