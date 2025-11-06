# 🔧 Correção do Erro "message larger than max"

## ❌ Problema
```
received message larger than max (6947732 vs 4194304)
```

Este erro ocorre quando mensagens gRPC excedem o limite padrão de 4MB.

## 🔍 Causa
- Imagens em base64 são ~33% maiores que o original
- Dados de análise celular podem ser extensos
- Limite padrão do gRPC: 4MB
- Imagens típicas: 5-10MB após processamento

## ✅ Solução Implementada

### 1. **Servidor Cellpose** (porta 50051)
```python
# api--microseg-model/server/grpc_server.py
options = [
    ('grpc.max_send_message_length', 50 * 1024 * 1024),  # 50MB
    ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 50MB
    ('grpc.max_message_length', 50 * 1024 * 1024),  # 50MB
]
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=options)
```

### 2. **Servidor Meditron** (porta 50052)
```python
# api--meditron-service/server/grpc_server.py
options = [
    ('grpc.max_send_message_length', 50 * 1024 * 1024),  # 50MB
    ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 50MB
    ('grpc.max_message_length', 50 * 1024 * 1024),  # 50MB
]
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=options)
```

### 3. **Cliente Go Service**
```go
// api--microseg-service/internal/handlers/image.go
opts := []grpc.DialOption{
    grpc.WithTransportCredentials(insecure.NewCredentials()),
    grpc.WithDefaultCallOptions(
        grpc.MaxCallRecvMsgSize(50*1024*1024), // 50MB
        grpc.MaxCallSendMsgSize(50*1024*1024), // 50MB
    ),
}
conn, err := grpc.NewClient(grpcServerAddr, opts...)
```

## 📊 Limites Configurados

| Componente | Limite Anterior | Limite Atual | Aumento |
|------------|-----------------|--------------|---------|
| Cellpose Server | 4MB | 50MB | 12.5x |
| Meditron Server | 4MB | 50MB | 12.5x |
| Go Client | 4MB | 50MB | 12.5x |

## 🎯 Benefícios

### ✅ **Suporte a Imagens Grandes**
- Imagens até ~35MB (considerando overhead base64)
- Suporte a imagens de alta resolução
- Margem de segurança para crescimento

### ✅ **Dados de Análise Extensos**
- Milhares de células analisadas
- Características detalhadas por célula
- Relatórios médicos completos

### ✅ **Performance Mantida**
- Limite aplicado apenas quando necessário
- Sem impacto em mensagens pequenas
- Timeout adequado para processamento

## 🧪 Teste da Correção

### 1. **Reiniciar Servidores**
```bash
# Terminal 1: Cellpose
cd api--microseg-model
python main.py

# Terminal 2: Meditron  
cd api--meditron-service
python main.py

# Terminal 3: Go Service
cd api--microseg-service
go run main.go
```

### 2. **Verificar Logs**
```
[CELLPOSE SERVER] Configurado para mensagens até 50MB
[MEDITRON SERVER] Configurado para mensagens até 50MB
```

### 3. **Testar com Imagem Grande**
- Upload de imagem de alta resolução
- Verificar processamento completo
- Confirmar análise médica gerada

## 📈 Monitoramento

### Logs de Sucesso:
```
[CELLPOSE SERVER] Processamento concluído. Células detectadas: X
[MEDITRON SERVER] Análise gerada com sucesso. Confiança: Y
[GO SERVICE] Processamento completo, total_cells: Z
```

### Possíveis Problemas:
- **Timeout**: Aumentar timeout se necessário
- **Memória**: Monitorar uso de RAM
- **Rede**: Verificar largura de banda

## 🔄 Rollback (se necessário)

Para voltar aos limites padrão, remover as opções:
```python
# Remover estas linhas dos servidores
options = [
    ('grpc.max_send_message_length', 50 * 1024 * 1024),
    ('grpc.max_receive_message_length', 50 * 1024 * 1024),
    ('grpc.max_message_length', 50 * 1024 * 1024),
]
```

## 🎯 Status

✅ **Cellpose Server**: Configurado para 50MB  
✅ **Meditron Server**: Configurado para 50MB  
✅ **Go Client**: Configurado para 50MB  
✅ **Pipeline Completo**: Suporte a mensagens grandes  

O erro "message larger than max" foi **resolvido** e o sistema agora suporta imagens e análises de qualquer tamanho razoável!
