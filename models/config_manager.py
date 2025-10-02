"""
🎛️ Config Manager - MODEL
Gerenciamento centralizado de configurações
"""

import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.carregar_config()
        
    def carregar_config(self):
        """Carrega configurações do arquivo JSON"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.config_padrao()
        except Exception as e:
            print(f"❌ Erro ao carregar configurações: {e}")
            return self.config_padrao()
    
    def salvar_config(self):
        """Salva configurações no arquivo JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar configurações: {e}")
            return False
    
    def config_padrao(self):
        """Retorna configuração padrão"""
        return {
            "model": {
                "path": "./modelo_treinado/best.pt",
                "fallback_path": "yolov8n-seg.pt",
                "confidence_threshold": 0.15,
                "iou_threshold": 0.5
            },
            "camera": {
                "device_id": 0,
                "resolution_width": 640,
                "resolution_height": 480,
                "fps_limit": 30
            },
            "display": {
                "show_masks": True,
                "show_boxes": True,
                "show_labels": True,
                "show_confidence": True,
                "show_fps": True,
                "window_title": "🎯 YOLO Detection Studio"
            },
            "tracking": {
                "enabled": True,
                "show_trails": True,
                "trail_length": 30,
                "tracker_type": "bytetrack"
            },
            "colors": {
                "detection_color": [0, 255, 0],
                "text_color": [255, 255, 255],
                "background_color": [0, 0, 0]
            },
            "precision": {
                "confidence_threshold_min": 0.25,
                "confidence_threshold_max": 0.8,
                "confidence_smoothing": True,
                "min_area_pixels": 500,
                "max_area_pixels": 50000,
                "area_filter": True,
                "stability_check": True,
                "stability_frames": 3,
                "nms_threshold": 0.4,
                "duplicate_threshold": 0.3
            }
        }
    
    def get(self, key_path, default=None):
        """Busca valor por caminho (ex: 'model.confidence_threshold')"""
        keys = key_path.split('.')
        value = self.config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path, value):
        """Define valor por caminho"""
        keys = key_path.split('.')
        config_ref = self.config
        try:
            for key in keys[:-1]:
                if key not in config_ref:
                    config_ref[key] = {}
                config_ref = config_ref[key]
            config_ref[keys[-1]] = value
            return True
        except Exception as e:
            print(f"❌ Erro ao definir configuração: {e}")
            return False
    
    def reset_to_default(self):
        """Restaura configurações padrão"""
        self.config = self.config_padrao()
        return self.salvar_config()