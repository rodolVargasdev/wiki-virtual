import os
import sys
from dotenv import load_dotenv

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.gemini_service import gemini_service

def test_gemini():
    """Probar servicio de Gemini"""
    
    print("🧪 Probando servicio de Gemini...")
    
    # 1. Probar conexión
    print("\n1. Probando conexión...")
    if gemini_service.test_connection():
        print("✅ Conexión exitosa")
    else:
        print("❌ Error de conexión")
        return
    
    # 2. Probar generación de respuesta
    print("\n2. Probando generación de respuesta...")
    
    test_queries = [
        "¿Qué es la inteligencia artificial?",
        "Explica cómo funcionan las redes neuronales",
        "¿Cuál es la diferencia entre machine learning y deep learning?"
    ]
    
    for query in test_queries:
        print(f"\n Pregunta: {query}")
        
        # Contexto de ejemplo
        context = """
        Artículo 1: Introducción a la Inteligencia Artificial
        Contenido: La inteligencia artificial es una rama de la informática que se enfoca en crear sistemas capaces de realizar tareas que normalmente requieren inteligencia humana...
        
        Artículo 2: Redes Neuronales
        Contenido: Las redes neuronales son modelos computacionales inspirados en el funcionamiento del cerebro humano...
        """
        
        answer = gemini_service.generate_answer(query, context)
        print(f"✅ Respuesta: {answer[:200]}...")
    
    print("\n�� Test de Gemini completado!")

if __name__ == "__main__":
    test_gemini()