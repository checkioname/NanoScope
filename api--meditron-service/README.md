# API Meditron Service

Serviço de análise médica usando o modelo Meditron para gerar interpretações textuais baseadas nos dados quantitativos extraídos pelo Cellpose.

## Funcionalidades

- **Análise Médica Automatizada**: Gera relatórios médicos baseados em dados citológicos
- **Avaliação de Risco**: Classifica amostras por nível de risco
- **Recomendações Clínicas**: Sugere próximos passos baseados nos achados
- **Interface gRPC**: Comunicação eficiente com outros serviços

## Arquitetura

```
Cellpose (dados quantitativos) → Meditron Service → Análise textual médica
```

## Instalação

```bash
cd api--meditron-service
pip install -r requirements.txt
```

## Uso

### Iniciar o servidor:
```bash
python main.py
```

O servidor rodará na porta **50052** (diferente do Cellpose que usa 50051).

### Estrutura de dados de entrada:
- **CellFeatures**: Características individuais das células
- **GlobalMetrics**: Métricas globais da amostra
- **ImageContext**: Contexto da amostra (ex: "breast tissue", "blood smear")

### Estrutura de dados de saída:
- **medical_analysis**: Análise médica detalhada
- **diagnosis_summary**: Resumo do diagnóstico
- **recommendations**: Recomendações clínicas
- **confidence_score**: Score de confiança (0-1)
- **key_findings**: Achados principais
- **risk_assessment**: Avaliação de risco

## Modelo

O serviço usa o **Meditron-7B** (versão otimizada) com:
- Quantização 4-bit para reduzir uso de memória
- Fallback para análise baseada em regras se o modelo não carregar
- Prompts médicos estruturados

## Integração

Para integrar com o pipeline principal:
1. O serviço Go chama o Cellpose
2. Com os dados do Cellpose, chama o Meditron
3. Retorna dados combinados para o frontend

## Portas

- **Cellpose**: 50051
- **Meditron**: 50052
- **Go Service**: 3000
- **Frontend**: 3000 (Next.js)

