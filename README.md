# 🎯 YOLO Detection Studio

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)
![YOLO](https://img.shields.io/badge/YOLO-v8-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**YOLO Detection Studio** é uma aplicação completa de detecção e contagem de objetos em tempo real usando YOLO (You Only Look Once) com interface gráfica intuitiva desenvolvida em Python.

## 🚀 Características Principais

- **🤖 Detecção em Tempo Real**: Utiliza YOLOv8 para detecção rápida e precisa
- **🎥 Suporte a Câmera**: Conecta-se automaticamente à webcam ou câmeras USB
- **🎛️ Interface Gráfica**: Interface moderna e intuitiva construída com Tkinter
- **⚙️ Configuração Flexível**: Parâmetros ajustáveis via interface e arquivo JSON
- **📊 Métricas em Tempo Real**: Contador de objetos, FPS e estatísticas
- **🎨 Visualização Avançada**: Bounding boxes, máscaras, confiança e trilhas
- **💾 Modelo Personalizado**: Suporte a modelos treinados customizados
- **🔧 Arquitetura MVC**: Código organizado e extensível

## 📋 Pré-requisitos

- **Python 3.8+** instalado no sistema
- **Webcam** ou câmera USB conectada
- **GPU** (opcional, mas recomendada para melhor performance)

## 🛠️ Instalação

### Instalação Automática (Windows)

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/yolo-detection-studio.git
cd yolo-detection-studio
```

2. **Execute o script de setup:**
```bash
setup.bat
```

O script irá automaticamente:
- Criar ambiente virtual Python
- Instalar todas as dependências
- Configurar o projeto
- Executar a aplicação

### Instalação Manual

1. **Clone o repositório:**
```bash
git clone https://github.com/rafaelmarinatoassis/yolo-detection-studio.git
cd yolo-detection-studio
```

2. **Crie um ambiente virtual:**
```bash
python -m venv .venv
```

3. **Ative o ambiente virtual:**
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

5. **Execute a aplicação:**
```bash
python app.py
```

## 🎮 Como Usar

### Interface Principal

A aplicação possui uma interface dividida em três áreas principais:

1. **🎥 Área de Vídeo**: Exibe o feed da câmera com detecções em tempo real
2. **🎛️ Painel de Controle**: Botões para iniciar/parar câmera e detecção
3. **⚙️ Configurações**: Ajustes de parâmetros do modelo e visualização

### Controles Básicos

- **▶️ Iniciar Câmera**: Conecta e inicia o feed da webcam
- **🎯 Iniciar Detecção**: Ativa a detecção de objetos
- **⏹️ Parar**: Para câmera e detecção
- **💾 Salvar Config**: Salva configurações atuais
- **❓ Ajuda**: Abre guia de uso rápido

### Atalhos de Teclado

- `Ctrl + S`: Salvar configurações
- `F1`: Mostrar ajuda

## ⚙️ Configuração

### Arquivo config.json

O arquivo `config.json` contém todas as configurações do sistema:

```json
{
  "model": {
    "path": "./modelo_treinado/best.pt",
    "confidence_threshold": 0.48,
    "iou_threshold": 0.29
  },
  "camera": {
    "device_id": 0,
    "resolution_width": 1920,
    "resolution_height": 1080,
    "fps_limit": 30
  },
  "display": {
    "show_masks": true,
    "show_boxes": true,
    "show_labels": true,
    "show_confidence": true,
    "show_fps": true
  }
}
```

### Modelo Personalizado

Para usar seu próprio modelo YOLO:

1. Coloque o arquivo `.pt` na pasta `modelo_treinado/`
2. Atualize o caminho em `config.json`:
```json
{
  "model": {
    "path": "./modelo_treinado/seu_modelo.pt"
  }
}
```

## 🏗️ Arquitetura do Projeto

O projeto segue o padrão **MVC (Model-View-Controller)**:

```
📁 YOLO Detection Studio/
├── 📄 app.py                    # Launcher principal
├── 📄 config.json              # Configurações
├── 📄 requirements.txt         # Dependências
├── 📄 setup.bat               # Script de instalação
├── 📁 controllers/
│   └── 📄 main_controller.py   # Controlador principal
├── 📁 models/
│   ├── 📄 detection_model.py   # Lógica de detecção YOLO
│   ├── 📄 camera_model.py      # Gerenciamento de câmera
│   └── 📄 config_manager.py    # Gerenciador de configurações
├── 📁 views/
│   └── 📄 main_interface.py    # Interface gráfica
└── 📁 modelo_treinado/
    └── 📄 best.pt             # Modelo YOLO personalizado
```

### Componentes Principais

- **🎮 MainController**: Orquestra a comunicação entre Model e View
- **🤖 DetectionModel**: Executa detecção YOLO e processamento
- **📹 CameraModel**: Gerencia captura e configuração da câmera
- **🖥️ MainInterface**: Interface gráfica e interação com usuário
- **⚙️ ConfigManager**: Carregamento e salvamento de configurações

## 📦 Dependências

### Principais
- **ultralytics**: Framework YOLO para detecção de objetos
- **opencv-python**: Processamento de imagem e vídeo
- **numpy**: Computação numérica
- **pillow**: Manipulação de imagens para GUI

### Interface
- **tkinter**: Interface gráfica (incluído no Python)

### Opcional
- **torch**: PyTorch (instalado automaticamente com ultralytics)
- **torchvision**: Visão computacional para PyTorch

## 🔧 Desenvolvimento

### Estrutura do Código

O projeto utiliza:
- **Padrão MVC** para separação de responsabilidades
- **Threading** para operações assíncronas
- **Configuração JSON** para flexibilidade
- **Tratamento de erros** robusto
- **Documentação** inline completa

### Adicionando Novas Funcionalidades

1. **Novos Modelos**: Adicione em `models/`
2. **Novos Controladores**: Adicione em `controllers/`
3. **Novas Views**: Adicione em `views/`
4. **Configurações**: Atualize `config.json` e `ConfigManager`

## 🐛 Solução de Problemas

### Problemas Comuns

**❌ "Python não encontrado"**
- Instale Python 3.8+ de [python.org](https://python.org)
- Adicione Python ao PATH do sistema

**❌ "Câmera não detectada"**
- Verifique se a câmera está conectada
- Teste diferentes valores para `device_id` (0, 1, 2...)
- Feche outros programas que usam a câmera

**❌ "Erro ao carregar modelo"**
- Verifique se o arquivo `best.pt` existe
- Baixe um modelo YOLO padrão se necessário
- Verifique conexão com internet para download automático

**❌ "Performance baixa"**
- Reduza a resolução da câmera
- Diminua o FPS limite
- Use uma GPU compatível com CUDA

### Logs e Debug

A aplicação mostra mensagens detalhadas no terminal:
- ✅ **Sucesso**: Operações concluídas
- ⚠️ **Aviso**: Situações não críticas
- ❌ **Erro**: Problemas que impedem execução

## 📊 Performance

### Benchmarks Típicos

| Hardware | FPS | Resolução |
|----------|-----|-----------|
| CPU Intel i5 | 15-25 FPS | 720p |
| CPU Intel i7 | 20-30 FPS | 1080p |
| GPU GTX 1060 | 45-60 FPS | 1080p |
| GPU RTX 3070 | 80-120 FPS | 1080p |

### Otimizações

- **GPU**: Use CUDA para melhor performance
- **Resolução**: Balance qualidade vs velocidade
- **Modelo**: Modelos menores = mais FPS
- **Confidence**: Thresholds maiores = menos processamento

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. **Push** para a branch (`git push origin feature/nova-feature`)
5. **Abra** um Pull Request

### Diretrizes

- Siga o padrão MVC existente
- Adicione documentação para novas funcionalidades
- Teste em diferentes ambientes
- Mantenha compatibilidade com Python 3.8+

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Rafael** - *Desenvolvedor Principal*

## 🙏 Agradecimentos

- **Ultralytics**: Framework YOLO excepcional
- **OpenCV**: Biblioteca de visão computacional
- **Python Community**: Ecossistema incrível de desenvolvimento

## 📞 Suporte

Para suporte e dúvidas:

- 📧 **Email**: seu-email@exemplo.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/seu-usuario/yolo-detection-studio/issues)
- 📖 **Wiki**: [Documentação Completa](https://github.com/seu-usuario/yolo-detection-studio/wiki)

---

⭐ **Se este projeto foi útil, considere dar uma estrela no GitHub!**