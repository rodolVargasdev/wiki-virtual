import google.generativeai as genai
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_available_models():
    """Probar modelos disponibles de Gemini"""
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY no encontrada")
        return
    
    # Configurar Gemini
    genai.configure(api_key=api_key)
    
    print("🔍 Modelos disponibles:")
    
    try:
        # Listar modelos disponibles
        models = genai.list_models()
        
        for model in models:
            print(f"   - {model.name}")
            print(f"     Display name: {model.display_name}")
            print(f"     Description: {model.description}")
            print(f"     Supported methods: {model.supported_generation_methods}")
            print()
            
    except Exception as e:
        print(f"❌ Error listando modelos: {str(e)}")

if __name__ == "__main__":
    test_available_models()