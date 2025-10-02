"""
📹 Camera Model - MODEL
Gerenciamento da câmera e captura de vídeo
"""

import cv2
import threading
import time
import numpy as np

class CameraModel:
    def __init__(self, config_manager):
        self.config = config_manager
        self.cap = None
        self.current_frame = None
        self.is_running = False
        self.capture_thread = None
        self.frame_lock = threading.Lock()
        
        # Configurações de imagem
        self.brightness = self.config.get('camera.brightness', 0)
        self.contrast = self.config.get('camera.contrast', 1.0)
        self.sharpness = self.config.get('camera.sharpness', 0)
        
    def start_camera(self):
        """Inicia captura da câmera"""
        try:
            device_id = self.config.get('camera.device_id', 0)
            self.cap = cv2.VideoCapture(device_id)
            
            if not self.cap.isOpened():
                print(f"❌ Não foi possível abrir a câmera {device_id}")
                return False
            
            # Configurar resolução
            width = self.config.get('camera.resolution_width', 640)
            height = self.config.get('camera.resolution_height', 480)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            
            # Configurar FPS se possível
            fps_limit = self.config.get('camera.fps_limit', 30)
            self.cap.set(cv2.CAP_PROP_FPS, fps_limit)
            
            self.is_running = True
            self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()
            
            print(f"✅ Câmera iniciada - {width}x{height} @ {fps_limit}fps")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao iniciar câmera: {e}")
            return False
    
    def stop_camera(self):
        """Para captura da câmera"""
        self.is_running = False
        
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=2.0)
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        with self.frame_lock:
            self.current_frame = None
        
        print("📹 Câmera parada")
    
    def _capture_loop(self):
        """Loop de captura em thread separada"""
        fps_limit = self.config.get('camera.fps_limit', 30)
        frame_time = 1.0 / fps_limit if fps_limit > 0 else 0
        
        while self.is_running and self.cap and self.cap.isOpened():
            start_time = time.time()
            
            ret, frame = self.cap.read()
            if ret:
                # Aplicar ajustes de imagem
                processed_frame = self._apply_image_adjustments(frame)
                
                with self.frame_lock:
                    self.current_frame = processed_frame.copy()
            else:
                print("⚠️ Falha na captura do frame")
            
            # Controle de FPS
            if frame_time > 0:
                elapsed = time.time() - start_time
                sleep_time = frame_time - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
    
    def _apply_image_adjustments(self, frame):
        """Aplica ajustes de brilho, contraste e nitidez ao frame"""
        if frame is None:
            return frame
        
        # Aplicar brilho e contraste
        adjusted = cv2.convertScaleAbs(frame, alpha=self.contrast, beta=self.brightness)
        
        # Aplicar nitidez (sharpening) se necessário
        if abs(self.sharpness) > 0.1:  # Evitar processamento desnecessário
            if self.sharpness > 0:
                # Kernel de nitidez para valores positivos
                kernel = np.array([[-1,-1,-1],
                                  [-1, 9 + self.sharpness,-1],
                                  [-1,-1,-1]])
            else:
                # Suavização para valores negativos (blur leve)
                blur_intensity = int(abs(self.sharpness) + 1)
                adjusted = cv2.GaussianBlur(adjusted, (blur_intensity*2+1, blur_intensity*2+1), 0)
                return adjusted
            
            adjusted = cv2.filter2D(adjusted, -1, kernel)
        
        return adjusted
    
    def get_frame(self):
        """Retorna o frame atual (thread-safe)"""
        with self.frame_lock:
            return self.current_frame.copy() if self.current_frame is not None else None
    
    def is_camera_running(self):
        """Verifica se a câmera está ativa"""
        return self.is_running and self.cap and self.cap.isOpened()
    
    def get_camera_info(self):
        """Retorna informações da câmera"""
        if not self.cap:
            return None
        
        return {
            'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': self.cap.get(cv2.CAP_PROP_FPS),
            'device_id': self.config.get('camera.device_id', 0)
        }
    
    def change_camera(self, device_id):
        """Troca para uma câmera diferente"""
        was_running = self.is_running
        
        if was_running:
            self.stop_camera()
        
        self.config.set('camera.device_id', device_id)
        
        if was_running:
            return self.start_camera()
        
        return True
    
    def update_brightness(self, value):
        """Atualiza brilho da imagem"""
        self.brightness = value
        self.config.set('camera.brightness', value)
    
    def update_contrast(self, value):
        """Atualiza contraste da imagem"""
        self.contrast = value
        self.config.set('camera.contrast', value)
    
    def update_sharpness(self, value):
        """Atualiza nitidez da imagem"""
        self.sharpness = value
        self.config.set('camera.sharpness', value)
    
    def get_image_settings(self):
        """Retorna configurações atuais de imagem"""
        return {
            'brightness': self.brightness,
            'contrast': self.contrast,
            'sharpness': self.sharpness
        }