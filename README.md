# 🎯 YOLO Detection Studio

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)
![YOLO](https://img.shields.io/badge/YOLO-v8-red.svg)
![Ultralytics](https://img.shields.io/badge/Ultralytics-8.0+-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**YOLO Detection Studio** é uma aplicação completa de detecção de objetos em tempo real usando YOLOv8 com segmentação avançada e interface gráfica intuitiva desenvolvida em Python. O sistema oferece detecção precisa, contagem automática de objetos e visualização em tempo real com arquitetura MVC robusta.

## 📸 Demonstração

> 💡 **Dica**: O sistema detecta automaticamente objetos em tempo real, exibindo bounding boxes coloridos, máscaras de segmentação semitransparentes e informações de confiança para cada detecção.

### Recursos Visuais
- 🎨 **Bounding Boxes**: Caixas coloridas ao redor dos objetos detectados
- 🎭 **Máscaras de Segmentação**: Sobreposição semitransparente delimitando objetos
- 🏷️ **Labels Dinâmicos**: Nome da classe e porcentagem de confiança
- 📊 **Estatísticas**: Contador de objetos e FPS em tempo real
- 🎛️ **Controles Intuitivos**: Interface responsiva para ajustes em tempo real

## 🚀 Características Principais

- **🤖 Detecção Avançada**: YOLOv8 com segmentação de instâncias e detecção de objetos
- **🎥 Suporte Multicâmera**: Conecta-se automaticamente à webcam ou câmeras USB/IP
- **🎛️ Interface Moderna**: GUI responsiva construída com Tkinter customizado
- **⚙️ Configuração Dinâmica**: Parâmetros ajustáveis em tempo real via interface
- **📊 Análise em Tempo Real**: Contador de objetos, FPS, confiança e estatísticas
- **🎨 Visualização Rica**: Bounding boxes, máscaras de segmentação, labels e confiança
- **💾 Modelos Personalizados**: Suporte completo a modelos YOLO treinados customizados
- **🔧 Arquitetura MVC**: Código modular, testável e facilmente extensível
- **🌟 Fallback Inteligente**: Sistema de fallback automático para modelos YOLOv8 padrão
- **🎯 Detecção Multi-classe**: Suporte a múltiplas classes de objetos simultaneamente

## 📋 Pré-requisitos

- **Python 3.8+** instalado no sistema
- **Webcam** ou câmera USB/IP conectada
- **4GB RAM** mínimo (8GB recomendado)
- **GPU CUDA** (opcional, mas recomendada para melhor performance)
- **Conexão com Internet** (para download automático de modelos)

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
- **🎯 Iniciar Detecção**: Ativa a detecção de objetos com segmentação
- **⏹️ Parar**: Para câmera e detecção
- **💾 Salvar Config**: Salva configurações atuais no arquivo JSON
- **🔄 Reset**: Restaura configurações padrão
- **❓ Ajuda**: Abre guia de uso rápido

### Atalhos de Teclado

- `Ctrl + S`: Salvar configurações
- `Ctrl + R`: Reset para configurações padrão
- `F1`: Mostrar ajuda
- `Esc`: Fechar aplicação

### Parâmetros Ajustáveis

- **Confidence Threshold**: Confiança mínima para detecção (0.0 - 1.0)
- **IoU Threshold**: Threshold de Intersection over Union (0.0 - 1.0)
- **Visualização**: Toggle para boxes, máscaras, labels e confiança
- **Configurações de Câmera**: Resolução, FPS, brilho, contraste

## ⚙️ Configuração

### Arquivo config.json

O arquivo `config.json` contém todas as configurações do sistema:

```json
{
  "model": {
    "path": "./modelo_treinado/best.pt",
    "fallback_path": "yolov8n-seg.pt",
    "confidence_threshold": 0.5038585209003216,
    "iou_threshold": 0.2980707395498392
  },
  "camera": {
    "device_id": 0,
    "resolution_width": 1920,
    "resolution_height": 1080,
    "fps_limit": 30,
    "brightness": 0,
    "contrast": 1.0,
    "sharpness": 0
  },
  "display": {
    "show_masks": true,
    "show_boxes": true,
    "show_labels": true,
    "show_confidence": true,
    "show_fps": true,
    "mask_alpha": 0.6,
    "line_thickness": 2
  }
}
```

### Modelo Personalizado

Para usar seu próprio modelo YOLO:

1. **Coloque o arquivo `.pt` na pasta `modelo_treinado/`**
2. **Atualize o caminho em `config.json`:**
```json
{
  "model": {
    "path": "./modelo_treinado/seu_modelo.pt",
    "fallback_path": "yolov8n-seg.pt"
  }
}
```

**Sistema de Fallback**: Se o modelo personalizado não for encontrado, o sistema automaticamente baixará e usará um modelo YOLOv8 padrão (yolov8n-seg.pt) da Ultralytics.

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
- **ultralytics>=8.0.0**: Framework YOLOv8 completo com segmentação
- **opencv-python>=4.5.0**: Processamento de imagem e vídeo
- **numpy>=1.21.0**: Computação numérica eficiente
- **pillow>=8.0.0**: Manipulação de imagens para GUI

### Interface
- **tkinter**: Interface gráfica (incluído no Python standard library)

### Automática (instaladas com ultralytics)
- **torch**: PyTorch para deep learning
- **torchvision**: Visão computacional para PyTorch
- **matplotlib**: Visualização de dados
- **tqdm**: Barras de progresso

## 🔧 Desenvolvimento

### Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **Ultralytics YOLOv8**: Detecção e segmentação de objetos
- **OpenCV**: Processamento de imagem e captura de vídeo
- **Tkinter**: Interface gráfica nativa do Python
- **NumPy**: Computação numérica eficiente
- **PyTorch**: Framework de deep learning (backend do YOLO)

### Estrutura do Código

O projeto utiliza:
- **Padrão MVC** para separação clara de responsabilidades
- **Threading** para operações assíncronas sem travamento da UI
- **Configuração JSON** para flexibilidade e persistência
- **Tratamento de erros** robusto com fallbacks
- **Type hints** para melhor documentação do código
- **Logging** estruturado para debug e monitoramento

### Adicionando Novas Funcionalidades

1. **Novos Modelos**: Adicione em `models/` seguindo o padrão existente
2. **Novos Controladores**: Adicione em `controllers/` com herança apropriada
3. **Novas Views**: Adicione em `views/` seguindo arquitetura tkinter
4. **Configurações**: Atualize `config.json` e `ConfigManager` correspondente
5. **Testes**: Adicione testes unitários para novas funcionalidades

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
- Verifique se o arquivo `best.pt` existe na pasta `modelo_treinado/`
- O sistema usará automaticamente um modelo YOLOv8 padrão se o modelo personalizado não for encontrado
- Verifique conexão com internet para download automático de modelos
- Certifique-se de que o modelo é compatível com YOLOv8

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

| Hardware | FPS | Resolução | Tipo de Modelo |
|----------|-----|-----------|----------------|
| CPU Intel i5 | 10-18 FPS | 720p | YOLOv8n |
| CPU Intel i7 | 15-25 FPS | 1080p | YOLOv8n |
| GPU GTX 1060 | 35-50 FPS | 1080p | YOLOv8s |
| GPU RTX 3070 | 60-90 FPS | 1080p | YOLOv8m |
| GPU RTX 4080 | 80-120 FPS | 1080p | YOLOv8l |

### Otimizações

- **GPU CUDA**: Use GPU compatível com CUDA para performance até 10x melhor
- **Resolução**: Balance qualidade vs velocidade (720p vs 1080p vs 4K)
- **Modelo**: YOLOv8n (rápido) vs YOLOv8l (preciso)
- **Thresholds**: Ajuste confidence/IOU para otimizar detecção vs performance
- **FPS Limit**: Configure limite de FPS baseado na capacidade do hardware

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

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

### Licenças de Terceiros
- **Ultralytics YOLOv8**: AGPL-3.0 License (para uso comercial, verifique licenciamento)
- **OpenCV**: Apache 2.0 License  
- **PyTorch**: BSD-style License

## 🔒 Compatibilidade

### Sistemas Operacionais
- ✅ **Windows 10/11** (Testado)
- ✅ **Linux Ubuntu 18.04+** (Compatível)
- ✅ **macOS 10.15+** (Compatível)

### Python Versions
- ✅ **Python 3.8** (Mínimo)
- ✅ **Python 3.9** (Recomendado)
- ✅ **Python 3.10** (Totalmente suportado)
- ✅ **Python 3.11** (Totalmente suportado)

## 👨‍💻 Autor

**Rafael Marinato Assis** - *Desenvolvedor Principal*
- 🐙 GitHub: [@rafaelmarinatoassis](https://github.com/rafaelmarinatoassis)
- 🌐 Repositório: [yolo-detection-studio](https://github.com/rafaelmarinatoassis/yolo-detection-studio)

## 🙏 Agradecimentos

- **Ultralytics**: Framework YOLOv8 excepcional com segmentação avançada
- **OpenCV**: Biblioteca de visão computacional robusta e versátil  
- **Python Community**: Ecossistema incrível de desenvolvimento
- **PyTorch**: Framework de deep learning poderoso e flexível

## 📞 Suporte

Para suporte e dúvidas:

-  **Issues**: [GitHub Issues](https://github.com/rafaelmarinatoassis/yolo-detection-studio/issues)
- 📖 **Documentação**: [README Completo](https://github.com/rafaelmarinatoassis/yolo-detection-studio#readme)
- 💬 **Discussões**: [GitHub Discussions](https://github.com/rafaelmarinatoassis/yolo-detection-studio/discussions)

## 🎯 Roadmap

### Próximas Funcionalidades
- [ ] **Gravação de Vídeo**: Salvar sessões de detecção
- [ ] **Múltiplas Câmeras**: Suporte a múltiplas fontes simultaneamente  
- [ ] **API REST**: Interface para integração externa
- [ ] **Dashboard Web**: Interface web complementar
- [ ] **Análise Offline**: Processamento de vídeos pré-gravados
- [ ] **Exportação de Dados**: Relatórios e estatísticas detalhadas

---

⭐ **Se este projeto foi útil, considere dar uma estrela no GitHub!**
