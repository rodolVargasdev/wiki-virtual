import requests
import json
from regenerate_token import regenerate_token

def test_complete_system_fresh():
    """Probar sistema completo con token fresco"""
    
    print("🧪 Probando sistema completo con token fresco...")
    
    # Regenerar token fresco
    token = regenerate_token()
    if not token:
        print("❌ No se pudo obtener token fresco")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    base_url = "http://localhost:8000"
    
    # 1. Verificar que la API está funcionando
    print("\n1. Verificando API...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ API funcionando correctamente")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Error en API: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error conectando con API: {str(e)}")
        return
    
    # 2. Crear artículo de prueba
    print("\n2. Creando artículo de prueba...")
    article_data = {
        "title": "Inteligencia Artificial con Gemini",
        "content": "La inteligencia artificial es una tecnología que permite a las máquinas realizar tareas que normalmente requieren inteligencia humana. Gemini es un modelo de IA desarrollado por Google que puede generar texto, responder preguntas y ayudar con diversas tareas. Es especialmente útil para aplicaciones educativas y de investigación.",
        "category": "Tecnología",
        "tags": ["IA", "Gemini", "Google", "educación"],
        "visibility": "public"
    }
    
    try:
        response = requests.post(f"{base_url}/articles/", json=article_data, headers=headers)
        if response.status_code == 200:
            article_id = response.json()["article_id"]
            print(f"✅ Artículo creado: {article_id}")
        else:
            print(f"❌ Error creando artículo: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error en creación de artículo: {str(e)}")
        return
    
    # 3. Probar chat con Gemini
    print("\n3. Probando chat con Gemini...")
    chat_requests = [
        "¿Qué es la inteligencia artificial?",
        "¿Qué es Gemini y para qué sirve?",
        "¿Cómo puede ayudar la IA en la educación?"
    ]
    
    for i, question in enumerate(chat_requests, 1):
        print(f"\n   Pregunta {i}: {question}")
        
        chat_data = {
            "message": question,
            "max_results": 3
        }
        
        try:
            response = requests.post(f"{base_url}/chat/", json=chat_data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Respuesta: {result['answer'][:150]}...")
                print(f"   📊 Confianza: {result['confidence']:.3f}")
                print(f"   �� Modelo: {result['model']}")
                print(f"   📚 Fuentes: {len(result['sources'])} artículos")
            else:
                print(f"   ❌ Error en chat: {response.text}")
        except Exception as e:
            print(f"   ❌ Error en chat: {str(e)}")
    
    print("\n�� Test del sistema completo con token fresco finalizado!")

if __name__ == "__main__":
    test_complete_system_fresh()