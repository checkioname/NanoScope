# 🔬 NanoScope - Pipeline Completo de Análise Celular

## 📋 Visão Geral

O NanoScope agora possui um pipeline completo de análise:

```
Imagem → Cellpose (segmentação) → Meditron (análise médica) → Frontend (visualização)
```

## 🏗️ Arquitetura

### Serviços:
1. **api--microseg-model** (Python, porta 50051): Cellpose para segmentação celular
2. **api--meditron-service** (Python, porta 50052): Meditron para análise médica
3. **api--microseg-service** (Go, porta 3000): Orquestrador principal
4. **app--nanoscope-front** (Next.js, porta 3000): Interface do usuário

### Fluxo de Dados:
1. Frontend envia imagem → Go Service
2. Go Service → Cellpose (dados quantitativos)
3. Go Service → Meditron (análise médica)
4. Go Service → Frontend (dados completos + imagem processada)

## 🚀 Como Executar

### 1. Iniciar Cellpose Service
```bash
cd api--microseg-model
pip install -r requirements.txt
python main.py
```
*Porta: 50051*

### 2. Iniciar Meditron Service
```bash
cd api--meditron-service
pip install -r requirements.txt
python main.py
```
*Porta: 50052*

### 3. Iniciar Go Service (Orquestrador)
```bash
cd api--microseg-service
go run main.go
```
*Porta: 3000*

### 4. Iniciar Frontend
```bash
cd app--nanoscope-front
npm install
npm run dev
```
*Porta: 3000 (Next.js)*

## 📊 Dados Retornados

### Frontend recebe:
```json
{
  "processedImage": "data:image/jpeg;base64,/9j/4AAQ...",
  "cellFeatures": [...],
  "globalMetrics": {
    "total_cells": 15,
    "potentially_malignant_cells": 3,
    "malignancy_percentage": 20.0,
    "cell_density_per_mm2": 125.5,
    "mean_cell_size": 45.2,
    "image_quality_score": 85.3
  },
  "medicalAnalysis": {
    "medical_analysis": "RELATÓRIO DE ANÁLISE CITOLÓGICA...",
    "diagnosis_summary": "Análise de 15 células com 20.0% de atipias",
    "recommendations": "RECOMENDAÇÕES CLÍNICAS:\n1. Revisão por patologista...",
    "confidence_score": 0.85,
    "key_findings": ["15 células analisadas", "20.0% de células atípicas"],
    "risk_assessment": "Risco moderado - Acompanhamento clínico recomendado"
  }
}
```

## 🎨 Interface do Usuário

### Funcionalidades:
- **Upload de imagem**: Drag & drop ou clique
- **Visualização**: Imagem processada com máscaras
- **Tabs de análise**:
  - **Métricas**: Dados quantitativos do Cellpose
  - **Análise Médica**: Interpretação do Meditron

### Componentes da Análise Médica:
- Resumo do diagnóstico
- Avaliação de risco (com cores: verde/amarelo/vermelho)
- Achados principais
- Recomendações clínicas
- Barra de confiança da análise

## 🔧 Configurações

### Portas:
- Cellpose: `50051`
- Meditron: `50052`
- Go Service: `3000`
- Frontend: `3000` (Next.js dev server)

### Modelos:
- **Cellpose**: `cyto` (modelo padrão para citologia)
- **Meditron**: `meditron-7b` (versão otimizada, com fallback para análise baseada em regras)

## 🧪 Testando o Sistema

1. Acesse `http://localhost:3000`
2. Faça upload de uma imagem de células
3. Aguarde o processamento (pode demorar alguns segundos)
4. Visualize:
   - Imagem processada com segmentação
   - Tab "Métricas" com dados quantitativos
   - Tab "Análise Médica" com interpretação clínica

## 🔍 Troubleshooting

### Problemas Comuns:

1. **Erro "Module not found: cellpose"**
   ```bash
   cd api--microseg-model
   pip install cellpose
   ```

2. **Erro de conexão gRPC**
   - Verifique se os serviços Python estão rodando
   - Confirme as portas 50051 e 50052

3. **Frontend não carrega dados**
   - Verifique se o Go service está na porta 3000
   - Confirme CORS no backend

4. **Meditron muito lento**
   - O sistema usa fallback baseado em regras se o modelo não carregar
   - Para produção, considere usar GPU ou modelo menor

## 📈 Próximos Passos

1. **Otimização**: Cache de modelos, processamento assíncrono
2. **Segurança**: Autenticação, validação de arquivos
3. **Escalabilidade**: Containerização, load balancing
4. **Funcionalidades**: Histórico de análises, exportação de relatórios

## 🎯 Resultado Final

O sistema agora oferece:
- ✅ Segmentação automática de células (Cellpose)
- ✅ Análise médica automatizada (Meditron)
- ✅ Interface intuitiva com tabs
- ✅ Visualização de dados quantitativos e qualitativos
- ✅ Avaliação de risco com código de cores
- ✅ Recomendações clínicas estruturadas

