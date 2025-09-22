import requests
import json
from test_auth import get_id_token

def test_rag_complete():
    """Probar sistema RAG completo"""
    
    # Obtener token de autenticación
    token = get_id_token("admin@example.com", "qw12QW")
    if not token:
        print("❌ No se pudo obtener token")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    base_url = "http://localhost:8000"
    
    # 1. Crear artículo de prueba
    print(" Creando artículo de prueba...")
    article_data = {
        "title": "Introducción a Redes de Computadoras",
        "content": "Las redes de computadoras son sistemas que permiten la comunicación entre dispositivos. Existen diferentes tipos de redes como LAN, WAN y MAN. Las redes utilizan protocolos como TCP/IP para la comunicación.",
        "category": "Tecnología",
        "tags": ["redes", "computación", "protocolos"],
        "visibility": "public"
    }
    
    response = requests.post(f"{base_url}/articles/", json=article_data, headers=headers)
    if response.status_code == 200:
        article_id = response.json()["article_id"]
        print(f"✅ Artículo creado: {article_id}")
    else:
        print(f"❌ Error creando artículo: {response.text}")
        return
    
    # 2. Probar chat con IA
    print("🧪 Probando chat con IA...")
    chat_requests = [
        "¿Qué son las redes de computadoras?",
        "¿Qué tipos de redes existen?",
        "¿Qué protocolos usan las redes?"
    ]
    
    for question in chat_requests:
        print(f"\n Pregunta: {question}")
        
        chat_data = {
            "message": question,
            "max_results": 3
        }
        
        response = requests.post(f"{base_url}/chat/", json=chat_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Respuesta: {result['answer']}")
            print(f" Confianza: {result['confidence']:.2f}")
            print(f" Fuentes: {len(result['sources'])} artículos")
        else:
            print(f"❌ Error en chat: {response.text}")
    
    # 3. Obtener estadísticas
    print("\n Obteniendo estadísticas...")
    response = requests.get(f"{base_url}/chat/stats", headers=headers)
    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Estadísticas: {stats}")
    else:
        print(f"❌ Error obteniendo estadísticas: {response.text}")

if __name__ == "__main__":
    test_rag_complete()