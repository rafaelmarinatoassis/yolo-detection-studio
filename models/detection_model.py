"""
🎯 Detection Model - MODEL 
Lógica de detecção e processamento YOLO
"""

import cv2
import numpy as np
from ultralytics import YOLO
from collections import deque
import time
import math
import os

class DetectionModel:
    def __init__(self, config_manager):
        self.config = config_manager
        self.model = self.carregar_modelo()
        
        # Métricas de performance
        self.fps_counter = 0
        self.start_time = time.time()
        self.fps_history = deque(maxlen=30)
        self.detection_history = deque(maxlen=10)
        
        # Sistema de tracking
        self.tracking_data = {}
        self.next_id = 1
        
    def carregar_modelo(self):
        """Carrega modelo YOLO"""
        try:
            # Tentar carregar modelo principal
            model_path = self.config.get('model.path')
            if os.path.exists(model_path):
                model = YOLO(model_path)
                print(f"✅ Modelo principal carregado: {model_path}")
                return model
            
            # Fallback para modelo padrão
            fallback_path = self.config.get('model.fallback_path')
            if os.path.exists(fallback_path):
                model = YOLO(fallback_path)
                print(f"⚠️ Usando modelo fallback: {fallback_path}")
                return model
            
            # Último recurso - baixar modelo
            print("📥 Baixando modelo padrão...")
            return YOLO('yolov8n-seg.pt')
            
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")
            return None
    
    def detectar(self, frame):
        """Executa detecção no frame"""
        if self.model is None:
            return frame, []
        
        try:
            # Executar predição
            results = self.model(
                frame,
                conf=self.config.get('model.confidence_threshold', 0.15),
                iou=self.config.get('model.iou_threshold', 0.5),
                verbose=False
            )
            
            detections = []
            annotated_frame = frame.copy()
            
            if results and len(results) > 0:
                result = results[0]
                
                # Processar detecções
                if result.boxes is not None and len(result.boxes) > 0:
                    for i, box in enumerate(result.boxes):
                        # Extrair dados da detecção
                        detection_data = self._processar_deteccao(box, result, i)
                        
                        if self._validar_deteccao(detection_data):
                            detections.append(detection_data)
                            annotated_frame = self._desenhar_deteccao(annotated_frame, detection_data)
            
            # Atualizar métricas
            self._atualizar_metricas(len(detections))
            
            return annotated_frame, detections
            
        except Exception as e:
            print(f"❌ Erro na detecção: {e}")
            return frame, []
    
    def _processar_deteccao(self, box, result, index):
        """Processa uma detecção individual"""
        # Coordenadas da bounding box
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        confidence = box.conf[0].cpu().numpy()
        
        # Obter classe (para modelo de classe única, sempre será 0)
        if hasattr(box, 'cls') and box.cls is not None:
            class_id = int(box.cls[0].cpu().numpy())
        else:
            class_id = 0
        
        # Calcular centro e área
        centro_x = int((x1 + x2) / 2)
        centro_y = int((y1 + y2) / 2)
        area = (x2 - x1) * (y2 - y1)
        
        detection_data = {
            'bbox': [int(x1), int(y1), int(x2), int(y2)],
            'confidence': float(confidence),
            'center': (centro_x, centro_y),
            'area': float(area),
            'class_id': class_id,
            'class_name': 'estator'  # Nome específico do modelo treinado
        }
        
        # Adicionar máscara se disponível
        if hasattr(result, 'masks') and result.masks is not None:
            if len(result.masks.data) > index:
                mask = result.masks.data[index].cpu().numpy()
                detection_data['mask'] = mask
        
        return detection_data
    
    def _validar_deteccao(self, detection):
        """Valida se a detecção atende aos critérios de qualidade"""
        # Filtro de confiança
        min_conf = self.config.get('precision.confidence_threshold_min', 0.01)
        max_conf = self.config.get('precision.confidence_threshold_max', 0.99)
        
        if not (min_conf <= detection['confidence'] <= max_conf):
            return False
        
        # Filtro de área
        if self.config.get('precision.area_filter', False):
            min_area = self.config.get('precision.min_area_pixels', 10)
            max_area = self.config.get('precision.max_area_pixels', 999999)
            
            if not (min_area <= detection['area'] <= max_area):
                return False
        
        return True
    
    def _desenhar_deteccao(self, frame, detection):
        """Desenha visualização da detecção"""
        x1, y1, x2, y2 = detection['bbox']
        confidence = detection['confidence']
        
        # Cores
        color = tuple(self.config.get('colors.detection_color', [0, 255, 0]))
        text_color = tuple(self.config.get('colors.text_color', [255, 255, 255]))
        
        # Desenhar bounding box
        if self.config.get('display.show_boxes', True):
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        # Desenhar label e confiança
        if self.config.get('display.show_labels', True) or self.config.get('display.show_confidence', True):
            label = ""
            if self.config.get('display.show_labels', True):
                label += detection['class_name']
            if self.config.get('display.show_confidence', True):
                if label:
                    label += f" {confidence:.2f}"
                else:
                    label = f"{confidence:.2f}"
            
            # Background do texto
            (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, (x1, y1 - text_height - 10), (x1 + text_width, y1), color, -1)
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
        
        # Desenhar máscara
        if self.config.get('display.show_masks', True) and 'mask' in detection:
            mask = detection['mask']
            
            # Verificar e ajustar dimensões da máscara
            if mask.shape != frame.shape[:2]:
                # Redimensionar máscara para combinar com o frame
                mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
            
            # Criar máscara colorida
            colored_mask = np.zeros_like(frame)
            colored_mask[:, :] = color
            
            # Aplicar máscara com verificação de dimensões
            try:
                mask_area = mask > 0.5
                if mask_area.shape == frame.shape[:2]:
                    frame[mask_area] = cv2.addWeighted(frame, 0.7, colored_mask, 0.3, 0)[mask_area]
                else:
                    print(f"DEBUG: Dimensões incompatíveis - mask: {mask_area.shape}, frame: {frame.shape[:2]}")
            except Exception as e:
                print(f"DEBUG: Erro ao aplicar máscara: {e}")
        
        return frame
    
    def _atualizar_metricas(self, num_detections):
        """Atualiza métricas de performance"""
        # Calcular FPS
        current_time = time.time()
        if hasattr(self, 'last_frame_time'):
            fps = 1.0 / (current_time - self.last_frame_time)
            self.fps_history.append(fps)
        self.last_frame_time = current_time
        
        # Histórico de detecções
        self.detection_history.append(num_detections)
    
    def get_fps(self):
        """Retorna FPS médio"""
        if len(self.fps_history) > 0:
            return sum(self.fps_history) / len(self.fps_history)
        return 0.0
    
    def get_detection_count(self):
        """Retorna contagem média de detecções"""
        if len(self.detection_history) > 0:
            return sum(self.detection_history) / len(self.detection_history)
        return 0.0
    
    def reload_model(self):
        """Recarrega o modelo (útil quando configurações mudam)"""
        self.model = self.carregar_modelo()
        return self.model is not None