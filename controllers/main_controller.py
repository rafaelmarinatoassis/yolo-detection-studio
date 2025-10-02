"""
🎮 Main Controller - CONTROLLER
Controlador principal da aplicação
"""

import threading
import time
from pathlib import Path
import sys
import os

# Adicionar diretórios aos paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.config_manager import ConfigManager
from models.detection_model import DetectionModel
from models.camera_model import CameraModel
from views.main_interface import MainInterface

class MainController:
    def __init__(self):
        # Inicializar models
        self.config_manager = ConfigManager()
        self.camera_model = CameraModel(self.config_manager)
        self.detection_model = DetectionModel(self.config_manager)
        
        # Estado da aplicação
        self.camera_running = False
        self.detection_running = False
        self.update_thread = None
        self.should_stop = False
        
        # Inicializar interface
        self.view = MainInterface(self)
        
        # Carregar configurações na UI
        self.view.load_config_to_ui(self.config_manager)
        
        # Iniciar thread de atualização da interface
        self.start_update_thread()
        
    def start_update_thread(self):
        """Inicia thread para atualizar interface"""
        self.should_stop = False
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()
    
    def _update_loop(self):
        """Loop principal de atualização"""
        while not self.should_stop:
            try:
                # Atualizar vídeo se câmera estiver ativa
                if self.camera_running:
                    frame = self.camera_model.get_frame()
                    
                    if frame is not None:
                        processed_frame = frame
                        detections = []
                        
                        # Aplicar detecção se ativa
                        if self.detection_running:
                            processed_frame, detections = self.detection_model.detectar(frame)
                        
                        # Atualizar interface
                        self.view.update_video_display(processed_frame)
                        
                        # Atualizar estatísticas
                        fps = self.detection_model.get_fps()
                        det_count = len(detections)
                        
                        self.view.update_status({
                            'fps': fps,
                            'detections': det_count,
                            'camera_status': 'Conectada' if self.camera_running else 'Desconectada'
                        })
                
                # Atualizar botões
                self.view.update_buttons(self.camera_running, self.detection_running)
                
                time.sleep(0.03)  # ~30 FPS
                
            except Exception as e:
                print(f"❌ Erro no loop de atualização: {e}")
                time.sleep(0.1)
    
    # Métodos de controle da câmera
    def toggle_camera(self):
        """Liga/desliga câmera"""
        if not self.camera_running:
            if self.camera_model.start_camera():
                self.camera_running = True
                self.view.log_message("📹 Câmera iniciada com sucesso")
            else:
                self.view.log_message("❌ Falha ao iniciar câmera")
        else:
            self.camera_model.stop_camera()
            self.camera_running = False
            self.detection_running = False
            self.view.log_message("📹 Câmera parada")
    
    def change_camera(self, device_id):
        """Troca câmera"""
        if self.camera_model.change_camera(device_id):
            self.view.log_message(f"📹 Câmera trocada para dispositivo {device_id}")
        else:
            self.view.log_message(f"❌ Falha ao trocar para câmera {device_id}")
    
    def change_resolution(self, width, height):
        """Altera resolução da câmera"""
        self.config_manager.set('camera.resolution_width', width)
        self.config_manager.set('camera.resolution_height', height)
        
        # Reiniciar câmera se estiver ativa
        if self.camera_running:
            self.camera_model.stop_camera()
            if self.camera_model.start_camera():
                self.view.log_message(f"📐 Resolução alterada para {width}x{height}")
            else:
                self.view.log_message("❌ Falha ao aplicar nova resolução")
    
    # Métodos de controle da detecção
    def toggle_detection(self):
        """Liga/desliga detecção"""
        if not self.detection_running:
            if self.camera_running:
                self.detection_running = True
                self.view.log_message("🎯 Detecção iniciada")
            else:
                self.view.log_message("❌ Inicie a câmera antes da detecção")
        else:
            self.detection_running = False
            self.view.log_message("🎯 Detecção parada")
    
    def update_confidence(self, value):
        """Atualiza threshold de confiança"""
        self.config_manager.set('model.confidence_threshold', value)
        self.view.log_message(f"🎯 Confiança atualizada: {value:.2f}")
    
    def update_iou(self, value):
        """Atualiza threshold IoU"""
        self.config_manager.set('model.iou_threshold', value)
        self.view.log_message(f"📏 IoU atualizado: {value:.2f}")
    
    def update_display_options(self, options):
        """Atualiza opções de visualização"""
        for key, value in options.items():
            self.config_manager.set(f'display.{key}', value)
        self.view.log_message("👁️ Opções de visualização atualizadas")
    
    def update_brightness(self, value):
        """Atualiza brilho da imagem"""
        self.camera_model.update_brightness(value)
        self.view.log_message(f"☀️ Brilho atualizado: {value:.0f}")
    
    def update_contrast(self, value):
        """Atualiza contraste da imagem"""
        self.camera_model.update_contrast(value)
        self.view.log_message(f"🔆 Contraste atualizado: {value:.2f}")
    
    def update_sharpness(self, value):
        """Atualiza nitidez da imagem"""
        self.camera_model.update_sharpness(value)
        self.view.log_message(f"🔍 Nitidez atualizada: {value:.1f}")
    
    def reset_image_settings(self):
        """Reseta configurações de imagem para valores padrão"""
        self.camera_model.update_brightness(0)
        self.camera_model.update_contrast(1.0)
        self.camera_model.update_sharpness(0)
        self.view.log_message("🎨 Configurações de imagem resetadas")
    
    def reload_model(self):
        """Recarrega o modelo"""
        if self.detection_model.reload_model():
            model_path = self.config_manager.get('model.path', 'N/A')
            self.view.model_path_label.config(text=f"Modelo: {model_path}")
            self.view.log_message("🤖 Modelo recarregado com sucesso")
        else:
            self.view.log_message("❌ Falha ao recarregar modelo")
    
    # Métodos de configuração
    def save_config(self):
        """Salva configurações"""
        if self.config_manager.salvar_config():
            self.view.log_message("💾 Configurações salvas com sucesso")
        else:
            self.view.log_message("❌ Falha ao salvar configurações")
    
    def reset_config(self):
        """Restaura configurações padrão"""
        if self.config_manager.reset_to_default():
            self.view.load_config_to_ui(self.config_manager)
            self.view.log_message("🔄 Configurações restauradas ao padrão")
        else:
            self.view.log_message("❌ Falha ao restaurar configurações")
    
    # Limpeza e finalização
    def cleanup(self):
        """Limpa recursos antes de fechar"""
        self.should_stop = True
        
        if self.camera_running:
            self.camera_model.stop_camera()
        
        # Salvar configurações automaticamente
        self.config_manager.salvar_config()
        
        print("🧹 Recursos limpos com sucesso")
    
    def run(self):
        """Executa a aplicação"""
        print("🎯 YOLO Detection Studio - Interface Gráfica")
        print("Iniciando aplicação...")
        
        try:
            self.view.run()
        except KeyboardInterrupt:
            print("\n⏹️ Interrompido pelo usuário")
        except Exception as e:
            print(f"❌ Erro na execução: {e}")
        finally:
            self.cleanup()

def main():
    """Função principal"""
    try:
        app = MainController()
        app.run()
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()