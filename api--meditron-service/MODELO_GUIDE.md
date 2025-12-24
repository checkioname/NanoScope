# 🤖 Guia de Modelos Leves para Análise Médica

## 🎯 Opções Disponíveis

### 1. **OpenAI GPT** (Recomendado - Melhor Qualidade)
- **Prós**: Excelente qualidade, respostas médicas precisas
- **Contras**: Requer API key paga, depende de internet
- **Custo**: ~$0.002 por análise
- **Setup**: 30 segundos

### 2. **Ollama Local** (Recomendado - Gratuito)
- **Prós**: Gratuito, roda localmente, boa qualidade
- **Contras**: Requer instalação do Ollama
- **Custo**: Gratuito
- **Setup**: 5 minutos

### 3. **HuggingFace Transformers** (Alternativa)
- **Prós**: Modelo pequeno (~117MB), roda localmente
- **Contras**: Qualidade limitada para análise médica
- **Custo**: Gratuito
- **Setup**: 2 minutos

### 4. **Análise Baseada em Regras** (Fallback)
- **Prós**: Sempre funciona, rápido, sem dependências
- **Contras**: Limitado, não usa IA
- **Custo**: Gratuito
- **Setup**: Imediato

## 🚀 Como Configurar

### Opção 1: OpenAI GPT (Mais Simples)

1. **Obter API Key**:
   - Vá para https://platform.openai.com/api-keys
   - Crie uma conta e gere uma API key
   - Adicione créditos (mínimo $5)

2. **Configurar**:
   ```bash
   # Definir variável de ambiente
   export OPENAI_API_KEY="sua-api-key-aqui"
   
   # Ou criar arquivo .env
   echo "OPENAI_API_KEY=sua-api-key-aqui" > .env
   ```

3. **Instalar dependência**:
   ```bash
   pip install openai requests
   ```

4. **Ativar no código**:
   ```python
   # Em server/grpc_server.py, linha 28:
   MODEL_TYPE = "openai"
   ```

### Opção 2: Ollama Local (Gratuito)

1. **Instalar Ollama**:
   ```bash
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Windows: baixar de https://ollama.ai/download
   ```

2. **Baixar modelo médico**:
   ```bash
   ollama pull llama3.2:1b  # Modelo pequeno (1.3GB)
   # ou
   ollama pull llama3.2:3b  # Modelo maior, melhor qualidade (2GB)
   ```

3. **Iniciar Ollama**:
   ```bash
   ollama serve
   ```

4. **Ativar no código**:
   ```python
   # Em server/grpc_server.py, linha 28:
   MODEL_TYPE = "ollama"
   ```

### Opção 3: HuggingFace (Simples)

1. **Instalar dependências**:
   ```bash
   pip install transformers torch
   ```

2. **Ativar no código**:
   ```python
   # Em server/grpc_server.py, linha 28:
   MODEL_TYPE = "huggingface"
   ```

### Opção 4: Regras (Já Funcionando)

- Não requer configuração adicional
- Já está ativo por padrão

## 📊 Comparação de Qualidade

| Modelo | Qualidade | Velocidade | Custo | Setup |
|--------|-----------|------------|-------|-------|
| OpenAI GPT | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 💰 | ⭐⭐⭐⭐⭐ |
| Ollama | ⭐⭐⭐⭐ | ⭐⭐⭐ | 🆓 | ⭐⭐⭐ |
| HuggingFace | ⭐⭐ | ⭐⭐⭐⭐⭐ | 🆓 | ⭐⭐⭐⭐ |
| Regras | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 🆓 | ⭐⭐⭐⭐⭐ |

## 🔧 Configuração Rápida (Recomendada)

### Para Desenvolvimento/Teste:
```python
MODEL_TYPE = "simple"  # Análise baseada em regras
```

### Para Produção com Qualidade:
```python
MODEL_TYPE = "openai"  # Requer API key
```

### Para Produção Gratuita:
```python
MODEL_TYPE = "ollama"  # Requer Ollama instalado
```

## 🧪 Testando os Modelos

1. **Editar configuração**:
   ```python
   # Em api--meditron-service/server/grpc_server.py
   MODEL_TYPE = "openai"  # ou "ollama", "huggingface", "simple"
   ```

2. **Reiniciar servidor**:
   ```bash
   cd api--meditron-service
   python main.py
   ```

3. **Testar no frontend**:
   - Faça upload de uma imagem
   - Veja a qualidade da análise médica

## 📝 Exemplo de Saída

### OpenAI GPT:
```
ANÁLISE CITOLÓGICA AUTOMATIZADA

INTERPRETAÇÃO DOS ACHADOS:
A análise revela 15 células com 20% apresentando características atípicas.
Observam-se irregularidades nucleares moderadas e aumento da razão 
núcleo/citoplasma em algumas células.

DIAGNÓSTICO DIFERENCIAL:
1. Processo reativo benigno
2. Displasia de baixo grau
3. Lesão pré-neoplásica

RECOMENDAÇÕES CLÍNICAS:
1. Acompanhamento em 6 meses
2. Correlação com dados clínicos
3. Considerar biópsia se progressão
```

### Análise por Regras:
```
ANÁLISE CITOLÓGICA - RISCO MODERADO

Análise de 15 células revelou 3 (20%) com características atípicas moderadas.

INTERPRETAÇÃO:
Presença de alterações celulares que podem representar processo 
reativo, displásico ou neoplásico inicial.

RECOMENDAÇÕES:
1. Acompanhamento clínico em 3-6 meses
2. Repetir citologia se persistência dos sintomas
```

## 🎯 Recomendação Final

**Para começar**: Use `MODEL_TYPE = "simple"` (já funciona)
**Para melhor qualidade**: Configure OpenAI GPT
**Para solução gratuita**: Configure Ollama

Todos os modelos retornam o mesmo formato JSON, então você pode trocar facilmente entre eles!
