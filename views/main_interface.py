"""
🖥️ Main Interface - VIEW
Interface gráfica principal unificada
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import time

class MainInterface:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.setup_window()
        self.setup_layout()
        self.setup_video_area()
        self.setup_control_panel()
        
        # Estado da interface
        self.current_photo = None
        
    def setup_window(self):
        """Configurar janela principal"""
        self.root.title("🎯 YOLO Detection Studio")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Centralizar janela
        self.center_window()
        
        # Protocolo de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Atalhos de teclado
        self.root.bind('<Control-s>', lambda e: self.controller.save_config())
        self.root.bind('<F1>', lambda e: self.show_help())
        
    def center_window(self):
        """Centraliza janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_layout(self):
        """Configurar layout principal"""
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Dividir em duas partes: vídeo (esquerda) e controles (direita)
        self.video_frame = ttk.LabelFrame(self.main_frame, text="📹 Área de Vídeo", padding=10)
        self.video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.control_frame = ttk.LabelFrame(self.main_frame, text="🎛️ Painel de Controle", padding=10)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        self.control_frame.config(width=350)
        
    def setup_video_area(self):
        """Configurar área de exibição do vídeo"""
        # Canvas para o vídeo
        self.video_canvas = tk.Canvas(self.video_frame, bg='black', width=640, height=480)
        self.video_canvas.pack(expand=True, fill=tk.BOTH)
        
        # Label de status
        self.status_label = ttk.Label(self.video_frame, text="📹 Câmera desconectada", font=('Arial', 10))
        self.status_label.pack(pady=(5, 0))
        
    def setup_control_panel(self):
        """Configurar painel de controles"""
        # Notebook para abas
        self.notebook = ttk.Notebook(self.control_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba Principal
        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="🎯 Principal")
        self.setup_main_tab()
        
        # Aba Detecção
        self.detection_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.detection_tab, text="🔍 Detecção")
        self.setup_detection_tab()
        
        # Aba Câmera
        self.camera_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.camera_tab, text="📹 Câmera")
        self.setup_camera_tab()
        
        # Aba Ajustes de Imagem
        self.image_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.image_tab, text="🎨 Imagem")
        self.setup_image_tab()
        
        # Aba Estatísticas
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="📊 Stats")
        self.setup_stats_tab()
        
    def setup_main_tab(self):
        """Aba principal com controles básicos"""
        # Instruções iniciais
        intro_frame = ttk.LabelFrame(self.main_tab, text="🚀 Como Começar", padding=10)
        intro_frame.pack(fill=tk.X, pady=(0, 10))
        
        intro_text = ttk.Label(intro_frame, text="1. Conecte a câmera\n2. Ajuste as configurações se necessário\n3. Inicie a detecção\n4. Use as abas para personalizar", 
                              font=('Arial', 9), foreground='darkgreen')
        intro_text.pack(anchor=tk.W)
        
        # Controles de câmera
        camera_frame = ttk.LabelFrame(self.main_tab, text="📹 Controles de Câmera", padding=10)
        camera_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.camera_button = ttk.Button(camera_frame, text="▶️ Iniciar Câmera", 
                                       command=self.controller.toggle_camera)
        self.camera_button.pack(fill=tk.X, pady=(0, 5))
        
        self.detection_button = ttk.Button(camera_frame, text="🎯 Iniciar Detecção", 
                                         command=self.controller.toggle_detection, state='disabled')
        self.detection_button.pack(fill=tk.X)
        
        # Dica de uso
        camera_tip = ttk.Label(camera_frame, text="💡 A detecção só funciona com a câmera ativa", 
                              font=('Arial', 8), foreground='blue')
        camera_tip.pack(anchor=tk.W, pady=(2, 0))
        
        # Status
        status_frame = ttk.LabelFrame(self.main_tab, text="📊 Status em Tempo Real", padding=10)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.fps_label = ttk.Label(status_frame, text="FPS: --", font=('Arial', 10, 'bold'))
        self.fps_label.pack(anchor=tk.W)
        
        self.detections_label = ttk.Label(status_frame, text="Detecções: --", font=('Arial', 10, 'bold'))
        self.detections_label.pack(anchor=tk.W)
        
        self.camera_status_label = ttk.Label(status_frame, text="Câmera: Desconectada")
        self.camera_status_label.pack(anchor=tk.W)
        
        # Dica de performance
        perf_tip = ttk.Label(status_frame, text="💡 FPS baixo? Tente reduzir a resolução ou ajustar threshold", 
                            font=('Arial', 8), foreground='blue', wraplength=300)
        perf_tip.pack(anchor=tk.W, pady=(2, 0))
        
        # Ações rápidas
        actions_frame = ttk.LabelFrame(self.main_tab, text="⚡ Ações Rápidas", padding=10)
        actions_frame.pack(fill=tk.X)
        
        ttk.Button(actions_frame, text="💾 Salvar Configurações", 
                  command=self.controller.save_config).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(actions_frame, text="🔄 Resetar Configurações", 
                  command=self.controller.reset_config).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(actions_frame, text="📖 Ajuda", 
                  command=self.show_help).pack(fill=tk.X)
        
        # Dica final
        final_tip = ttk.Label(actions_frame, text="💡 Use Ctrl+S para salvar rapidamente as configurações", 
                             font=('Arial', 8), foreground='blue')
        final_tip.pack(anchor=tk.W, pady=(2, 0))
    
    def setup_detection_tab(self):
        """Aba de configurações de detecção"""
        # Confiança
        conf_frame = ttk.LabelFrame(self.detection_tab, text="🎯 Confiança", padding=10)
        conf_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Explicação da confiança
        conf_info = ttk.Label(conf_frame, text="Quão confiante o modelo deve estar para detectar um objeto.\nBaixo: mais detecções, menos precisão | Alto: menos detecções, mais precisão", 
                             font=('Arial', 8), foreground='gray', wraplength=300)
        conf_info.pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Label(conf_frame, text="Threshold:").pack(anchor=tk.W)
        self.confidence_var = tk.DoubleVar(value=0.15)
        self.confidence_scale = ttk.Scale(conf_frame, from_=0.1, to=0.9, 
                                         variable=self.confidence_var, orient=tk.HORIZONTAL,
                                         command=self.on_confidence_change)
        self.confidence_scale.pack(fill=tk.X)
        self.confidence_label = ttk.Label(conf_frame, text="0.15")
        self.confidence_label.pack(anchor=tk.W)
        
        # Dica de uso
        conf_tip = ttk.Label(conf_frame, text="💡 Dica: Comece com 0.3 e ajuste conforme necessário", 
                            font=('Arial', 8), foreground='blue')
        conf_tip.pack(anchor=tk.W, pady=(2, 0))
        
        # IoU
        iou_frame = ttk.LabelFrame(self.detection_tab, text="📏 IoU (Sobreposição)", padding=10)
        iou_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Explicação do IoU
        iou_info = ttk.Label(iou_frame, text="Controla detecções sobrepostas do mesmo objeto.\nBaixo: pode duplicar objetos | Alto: pode perder detecções válidas", 
                            font=('Arial', 8), foreground='gray', wraplength=300)
        iou_info.pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Label(iou_frame, text="Threshold:").pack(anchor=tk.W)
        self.iou_var = tk.DoubleVar(value=0.5)
        self.iou_scale = ttk.Scale(iou_frame, from_=0.1, to=0.9, 
                                  variable=self.iou_var, orient=tk.HORIZONTAL,
                                  command=self.on_iou_change)
        self.iou_scale.pack(fill=tk.X)
        self.iou_label = ttk.Label(iou_frame, text="0.50")
        self.iou_label.pack(anchor=tk.W)
        
        # Dica de uso
        iou_tip = ttk.Label(iou_frame, text="💡 Dica: 0.5 é um bom valor inicial para a maioria dos casos", 
                           font=('Arial', 8), foreground='blue')
        iou_tip.pack(anchor=tk.W, pady=(2, 0))
        
        # Visualização
        display_frame = ttk.LabelFrame(self.detection_tab, text="👁️ Visualização", padding=10)
        display_frame.pack(fill=tk.X)
        
        # Explicação da visualização
        display_info = ttk.Label(display_frame, text="Escolha o que mostrar na tela durante a detecção:", 
                                font=('Arial', 8), foreground='gray')
        display_info.pack(anchor=tk.W, pady=(0, 5))
        
        self.show_boxes_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(display_frame, text="Mostrar Caixas", 
                       variable=self.show_boxes_var,
                       command=self.on_display_change).pack(anchor=tk.W)
        
        self.show_masks_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(display_frame, text="Mostrar Máscaras", 
                       variable=self.show_masks_var,
                       command=self.on_display_change).pack(anchor=tk.W)
        
        self.show_confidence_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(display_frame, text="Mostrar Confiança", 
                       variable=self.show_confidence_var,
                       command=self.on_display_change).pack(anchor=tk.W)
    
    def setup_camera_tab(self):
        """Aba de configurações de câmera"""
        # Dispositivo
        device_frame = ttk.LabelFrame(self.camera_tab, text="📱 Dispositivo", padding=10)
        device_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Explicação do dispositivo
        device_info = ttk.Label(device_frame, text="Selecione qual câmera usar (0 = padrão, 1,2,3... = câmeras adicionais).\nTeste diferentes valores se a câmera não funcionar.", 
                               font=('Arial', 8), foreground='gray', wraplength=300)
        device_info.pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Label(device_frame, text="ID da Câmera:").pack(anchor=tk.W)
        self.device_var = tk.StringVar(value="0")
        device_combo = ttk.Combobox(device_frame, textvariable=self.device_var, 
                                   values=["0", "1", "2", "3"], width=10)
        device_combo.pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Button(device_frame, text="🔄 Trocar Câmera", 
                  command=self.change_camera).pack(fill=tk.X)
        
        # Dica de uso
        device_tip = ttk.Label(device_frame, text="💡 Dica: Pare a câmera antes de trocar de dispositivo", 
                              font=('Arial', 8), foreground='blue')
        device_tip.pack(anchor=tk.W, pady=(2, 0))
        
        # Resolução
        resolution_frame = ttk.LabelFrame(self.camera_tab, text="📐 Resolução", padding=10)
        resolution_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Explicação da resolução
        res_info = ttk.Label(resolution_frame, text="Define o tamanho da imagem capturada.\nMaior resolução = melhor qualidade, mas pode ser mais lenta.", 
                            font=('Arial', 8), foreground='gray', wraplength=300)
        res_info.pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Label(resolution_frame, text="Largura:").pack(anchor=tk.W)
        self.width_var = tk.StringVar(value="640")
        ttk.Entry(resolution_frame, textvariable=self.width_var, width=10).pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Label(resolution_frame, text="Altura:").pack(anchor=tk.W)
        self.height_var = tk.StringVar(value="480")
        ttk.Entry(resolution_frame, textvariable=self.height_var, width=10).pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Button(resolution_frame, text="✅ Aplicar Resolução", 
                  command=self.change_resolution).pack(fill=tk.X)
        
        # Dicas de resolução
        res_tip = ttk.Label(resolution_frame, text="💡 Resoluções comuns: 640x480 (rápido), 1280x720 (HD), 1920x1080 (Full HD)", 
                           font=('Arial', 8), foreground='blue', wraplength=300)
        res_tip.pack(anchor=tk.W, pady=(2, 0))
    
    def setup_image_tab(self):
        """Aba de ajustes de imagem"""
        # Brilho
        brightness_frame = ttk.LabelFrame(self.image_tab, text="☀️ Brilho", padding=10)
        brightness_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Explicação do brilho
        bright_info = ttk.Label(brightness_frame, text="Controla a luminosidade geral da imagem.\nNegativo: mais escuro | Positivo: mais claro", 
                               font=('Arial', 8), foreground='gray', wraplength=300)
        bright_info.pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Label(brightness_frame, text="Ajuste (-100 a +100):").pack(anchor=tk.W)
        self.brightness_var = tk.DoubleVar(value=0)
        self.brightness_scale = ttk.Scale(brightness_frame, from_=-100, to=100, 
                                         variable=self.brightness_var, orient=tk.HORIZONTAL,
                                         command=self.on_brightness_change)
        self.brightness_scale.pack(fill=tk.X)
        self.brightness_label = ttk.Label(brightness_frame, text="0")
        self.brightness_label.pack(anchor=tk.W)
        
        # Dica de uso
        bright_tip = ttk.Label(brightness_frame, text="💡 Dica: Ajuste conforme iluminação do ambiente", 
                              font=('Arial', 8), foreground='blue')
        bright_tip.pack(anchor=tk.W, pady=(2, 0))
        
        # Contraste
        contrast_frame = ttk.LabelFrame(self.image_tab, text="🔆 Contraste", padding=10)
        contrast_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Explicação do contraste
        contrast_info = ttk.Label(contrast_frame, text="Diferença entre cores claras e escuras.\nBaixo: imagem acinzentada | Alto: cores mais vívidas", 
                                 font=('Arial', 8), foreground='gray', wraplength=300)
        contrast_info.pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Label(contrast_frame, text="Ajuste (0.5 a 3.0):").pack(anchor=tk.W)
        self.contrast_var = tk.DoubleVar(value=1.0)
        self.contrast_scale = ttk.Scale(contrast_frame, from_=0.5, to=3.0, 
                                       variable=self.contrast_var, orient=tk.HORIZONTAL,
                                       command=self.on_contrast_change)
        self.contrast_scale.pack(fill=tk.X)
        self.contrast_label = ttk.Label(contrast_frame, text="1.0")
        self.contrast_label.pack(anchor=tk.W)
        
        # Dica de uso
        contrast_tip = ttk.Label(contrast_frame, text="💡 Dica: 1.0 é neutro, aumente para câmeras com pouco contraste", 
                                font=('Arial', 8), foreground='blue')
        contrast_tip.pack(anchor=tk.W, pady=(2, 0))
        
        # Nitidez
        sharpness_frame = ttk.LabelFrame(self.image_tab, text="🔍 Nitidez", padding=10)
        sharpness_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Explicação da nitidez
        sharp_info = ttk.Label(sharpness_frame, text="Define a clareza dos detalhes na imagem.\nNegativo: suaviza (blur) | Positivo: realça bordas", 
                              font=('Arial', 8), foreground='gray', wraplength=300)
        sharp_info.pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Label(sharpness_frame, text="Ajuste (-2 a +5):").pack(anchor=tk.W)
        self.sharpness_var = tk.DoubleVar(value=0)
        self.sharpness_scale = ttk.Scale(sharpness_frame, from_=-2, to=5, 
                                        variable=self.sharpness_var, orient=tk.HORIZONTAL,
                                        command=self.on_sharpness_change)
        self.sharpness_scale.pack(fill=tk.X)
        self.sharpness_label = ttk.Label(sharpness_frame, text="0")
        self.sharpness_label.pack(anchor=tk.W)
        
        # Dica de uso
        sharp_tip = ttk.Label(sharpness_frame, text="💡 Dica: Use com moderação, valores altos podem criar ruído", 
                             font=('Arial', 8), foreground='blue')
        sharp_tip.pack(anchor=tk.W, pady=(2, 0))
        
        # Botões de controle
        controls_frame = ttk.LabelFrame(self.image_tab, text="🎛️ Controles", padding=10)
        controls_frame.pack(fill=tk.X)
        
        control_info = ttk.Label(controls_frame, text="Ajustes aplicados em tempo real. Use Reset se a imagem ficar muito alterada.", 
                                font=('Arial', 8), foreground='gray', wraplength=300)
        control_info.pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Button(controls_frame, text="🔄 Resetar Ajustes", 
                  command=self.reset_image_settings).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(controls_frame, text="💾 Salvar Configurações", 
                  command=self.save_image_settings).pack(fill=tk.X)
    
    def setup_stats_tab(self):
        """Aba de estatísticas"""
        # Performance
        perf_frame = ttk.LabelFrame(self.stats_tab, text="⚡ Performance", padding=10)
        perf_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.avg_fps_label = ttk.Label(perf_frame, text="FPS Médio: --")
        self.avg_fps_label.pack(anchor=tk.W)
        
        self.avg_detections_label = ttk.Label(perf_frame, text="Detecções/Frame: --")
        self.avg_detections_label.pack(anchor=tk.W)
        
        # Modelo
        model_frame = ttk.LabelFrame(self.stats_tab, text="🤖 Modelo", padding=10)
        model_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.model_path_label = ttk.Label(model_frame, text="Carregando...", wraplength=300)
        self.model_path_label.pack(anchor=tk.W)
        
        ttk.Button(model_frame, text="🔄 Recarregar Modelo", 
                  command=self.controller.reload_model).pack(fill=tk.X, pady=(5, 0))
        
        # Logs
        log_frame = ttk.LabelFrame(self.stats_tab, text="📝 Logs", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_frame, height=8, width=40, font=('Consolas', 9))
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Event handlers
    def on_confidence_change(self, value):
        """Atualiza threshold de confiança"""
        conf_value = float(value)
        self.confidence_label.config(text=f"{conf_value:.2f}")
        self.controller.update_confidence(conf_value)
    
    def on_iou_change(self, value):
        """Atualiza threshold IoU"""
        iou_value = float(value)
        self.iou_label.config(text=f"{iou_value:.2f}")
        self.controller.update_iou(iou_value)
    
    def on_display_change(self):
        """Atualiza opções de visualização"""
        self.controller.update_display_options({
            'show_boxes': self.show_boxes_var.get(),
            'show_masks': self.show_masks_var.get(),
            'show_confidence': self.show_confidence_var.get()
        })
    
    def change_camera(self):
        """Troca câmera"""
        device_id = int(self.device_var.get())
        self.controller.change_camera(device_id)
    
    def change_resolution(self):
        """Altera resolução"""
        try:
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            self.controller.change_resolution(width, height)
        except ValueError:
            messagebox.showerror("Erro", "Resolução inválida!")
    
    def on_brightness_change(self, value):
        """Atualiza brilho"""
        brightness_value = float(value)
        self.brightness_label.config(text=f"{brightness_value:.0f}")
        self.controller.update_brightness(brightness_value)
    
    def on_contrast_change(self, value):
        """Atualiza contraste"""
        contrast_value = float(value)
        self.contrast_label.config(text=f"{contrast_value:.2f}")
        self.controller.update_contrast(contrast_value)
    
    def on_sharpness_change(self, value):
        """Atualiza nitidez"""
        sharpness_value = float(value)
        self.sharpness_label.config(text=f"{sharpness_value:.1f}")
        self.controller.update_sharpness(sharpness_value)
    
    def reset_image_settings(self):
        """Reseta configurações de imagem para padrão"""
        self.brightness_var.set(0)
        self.contrast_var.set(1.0)
        self.sharpness_var.set(0)
        self.controller.reset_image_settings()
    
    def save_image_settings(self):
        """Salva configurações de imagem"""
        self.controller.save_config()
    
    def show_help(self):
        """Mostra ajuda"""
        help_text = """🎯 YOLO Detection Studio - Guia Rápido

📹 CÂMERA:
• Use 'Iniciar Câmera' para conectar
• Troque entre câmeras na aba Câmera
• Ajuste resolução conforme necessário

🔍 DETECÇÃO:
• Confidence: quão confiante o modelo deve estar
  - Baixo (0.1-0.3): mais detecções, menos precisão
  - Alto (0.5-0.9): menos detecções, mais precisão
• IoU: controla sobreposições de detecções
  - 0.5 é um bom valor para maioria dos casos

🎨 AJUSTES DE IMAGEM:
• Brilho: -100 a +100 (padrão: 0)
• Contraste: 0.5 a 3.0 (padrão: 1.0)
• Nitidez: -2 a +5 (padrão: 0)
• Todos aplicados em tempo real

⌨️ ATALHOS:
• Ctrl+S: Salvar configurações rapidamente
• F1: Mostrar esta ajuda

⚙️ DICAS:
• Comece com valores padrão e ajuste gradualmente
• FPS baixo? Reduza resolução ou aumente threshold
• Use 'Reset' se algo der errado
• Configurações são salvas automaticamente"""
        messagebox.showinfo("Ajuda - YOLO Detection Studio", help_text)
    
    def update_video_display(self, frame):
        """Atualiza display de vídeo"""
        if frame is None:
            return
        
        try:
            # Converter BGR para RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Redimensionar para canvas
            canvas_width = self.video_canvas.winfo_width()
            canvas_height = self.video_canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:
                # Manter proporção
                h, w = frame_rgb.shape[:2]
                aspect_ratio = w / h
                
                if canvas_width / canvas_height > aspect_ratio:
                    new_height = canvas_height
                    new_width = int(canvas_height * aspect_ratio)
                else:
                    new_width = canvas_width
                    new_height = int(canvas_width / aspect_ratio)
                
                frame_resized = cv2.resize(frame_rgb, (new_width, new_height))
                
                # Converter para ImageTk
                image = Image.fromarray(frame_resized)
                self.current_photo = ImageTk.PhotoImage(image)
                
                # Centralizar no canvas
                x = (canvas_width - new_width) // 2
                y = (canvas_height - new_height) // 2
                
                self.video_canvas.delete("all")
                self.video_canvas.create_image(x, y, anchor=tk.NW, image=self.current_photo)
        
        except Exception as e:
            print(f"❌ Erro ao atualizar vídeo: {e}")
    
    def update_status(self, status_data):
        """Atualiza informações de status"""
        if 'fps' in status_data:
            fps = status_data['fps']
            self.fps_label.config(text=f"FPS: {fps:.1f}")
            self.avg_fps_label.config(text=f"FPS Médio: {fps:.1f}")
        
        if 'detections' in status_data:
            det_count = status_data['detections']
            self.detections_label.config(text=f"Detecções: {det_count}")
            self.avg_detections_label.config(text=f"Detecções/Frame: {det_count:.1f}")
        
        if 'camera_status' in status_data:
            cam_status = status_data['camera_status']
            self.camera_status_label.config(text=f"Câmera: {cam_status}")
            if cam_status == "Conectada":
                self.status_label.config(text="📹 Câmera conectada")
                self.detection_button.config(state='normal')
            else:
                self.status_label.config(text="📹 Câmera desconectada")
                self.detection_button.config(state='disabled')
    
    def update_buttons(self, camera_running, detection_running):
        """Atualiza estado dos botões"""
        if camera_running:
            self.camera_button.config(text="⏹️ Parar Câmera")
        else:
            self.camera_button.config(text="▶️ Iniciar Câmera")
            
        if detection_running:
            self.detection_button.config(text="⏹️ Parar Detecção")
        else:
            self.detection_button.config(text="🎯 Iniciar Detecção")
    
    def load_config_to_ui(self, config_manager):
        """Carrega configurações na interface"""
        # Detecção
        conf = config_manager.get('model.confidence_threshold', 0.15)
        self.confidence_var.set(conf)
        self.confidence_label.config(text=f"{conf:.2f}")
        
        iou = config_manager.get('model.iou_threshold', 0.5)
        self.iou_var.set(iou)
        self.iou_label.config(text=f"{iou:.2f}")
        
        # Display
        self.show_boxes_var.set(config_manager.get('display.show_boxes', True))
        self.show_masks_var.set(config_manager.get('display.show_masks', True))
        self.show_confidence_var.set(config_manager.get('display.show_confidence', True))
        
        # Câmera
        self.device_var.set(str(config_manager.get('camera.device_id', 0)))
        self.width_var.set(str(config_manager.get('camera.resolution_width', 640)))
        self.height_var.set(str(config_manager.get('camera.resolution_height', 480)))
        
        # Configurações de imagem
        brightness = config_manager.get('camera.brightness', 0)
        self.brightness_var.set(brightness)
        self.brightness_label.config(text=f"{brightness:.0f}")
        
        contrast = config_manager.get('camera.contrast', 1.0)
        self.contrast_var.set(contrast)
        self.contrast_label.config(text=f"{contrast:.2f}")
        
        sharpness = config_manager.get('camera.sharpness', 0)
        self.sharpness_var.set(sharpness)
        self.sharpness_label.config(text=f"{sharpness:.1f}")
        
        # Modelo
        model_path = config_manager.get('model.path', 'N/A')
        self.model_path_label.config(text=f"Modelo: {model_path}")
    
    def log_message(self, message):
        """Adiciona mensagem ao log"""
        timestamp = time.strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Limitar tamanho do log
        lines = int(self.log_text.index('end-1c').split('.')[0])
        if lines > 100:
            self.log_text.delete('1.0', '20.0')
    
    def on_closing(self):
        """Tratamento de fechamento da janela"""
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.controller.cleanup()
            self.root.destroy()
    
    def run(self):
        """Executa a interface"""
        self.root.mainloop()