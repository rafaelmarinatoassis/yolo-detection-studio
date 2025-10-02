"""
🎯 YOLO Detection Studio - Aplicação Principal
Launcher único e simplificado com arquitetura MVC
"""

import sys
import os
from pathlib import Path

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Função principal da aplicação"""
    try:
        # Verificar dependências
        print("🔍 Verificando dependências...")
        
        # Criar pasta modelo_treinado se não existir
        modelo_dir = "./modelo_treinado"
        if not os.path.exists(modelo_dir):
            os.makedirs(modelo_dir, exist_ok=True)
            print(f"📁 Pasta criada automaticamente: {modelo_dir}")
        
        # Importar e executar controlador principal
        from controllers.main_controller import MainController
        
        # Criar e executar aplicação
        app = MainController()
        app.run()
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Certifique-se de que todas as dependências estão instaladas")
        print("   Execute: pip install ultralytics opencv-python pillow")
        input("Pressione Enter para sair...")
        
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()