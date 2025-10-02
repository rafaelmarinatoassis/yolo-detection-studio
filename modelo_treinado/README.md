# Pasta para Modelos Treinados

Esta pasta deverá conter os modelos YOLO treinados personalizados.

## Estrutura:
- `best.pt` - Modelo principal treinado (arquivo grande, não versionado)
- Outros arquivos `.pt` - Modelos adicionais (não versionados)

## Nota:
Os arquivos `.pt` são ignorados pelo Git devido ao tamanho (geralmente 50MB+).
Para usar seus próprios modelos, coloque-os nesta pasta e atualize o `config.json`.