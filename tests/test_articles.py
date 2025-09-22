import requests
import json
from test_auth import get_id_token

def test_articles_crud():
    """Probar CRUD completo de artículos"""
    
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
    
    # 1. Crear artículo
    print("🧪 Creando artículo...")
    article_data = {
        "title": "Introducción a Redes de Computadoras",
        "content": "Las redes de computadoras son sistemas que permiten la comunicación entre dispositivos...",
        "category": "Tecnología",
        "tags": ["redes", "computación", "básico"],
        "visibility": "public"
    }
    
    response = requests.post(f"{base_url}/articles/", json=article_data, headers=headers)
    if response.status_code == 200:
        article_id = response.json()["article_id"]
        print(f"✅ Artículo creado: {article_id}")
    else:
        print(f"❌ Error creando artículo: {response.text}")
        return
    
    # 2. Listar artículos
    print("�� Listando artículos...")
    response = requests.get(f"{base_url}/articles/", headers=headers)
    if response.status_code == 200:
        articles = response.json()
        print(f"✅ {len(articles['articles'])} artículos encontrados")
    else:
        print(f"❌ Error listando artículos: {response.text}")
    
    # 3. Obtener artículo específico
    print("🧪 Obteniendo artículo específico...")
    response = requests.get(f"{base_url}/articles/{article_id}", headers=headers)
    if response.status_code == 200:
        article = response.json()
        print(f"✅ Artículo obtenido: {article['title']}")
    else:
        print(f"❌ Error obteniendo artículo: {response.text}")
    
    # 4. Actualizar artículo
    print("🧪 Actualizando artículo...")
    update_data = {
        "title": "Introducción a Redes de Computadoras - Actualizado",
        "content": "Las redes de computadoras son sistemas avanzados que permiten la comunicación entre dispositivos..."
    }
    
    response = requests.put(f"{base_url}/articles/{article_id}", json=update_data, headers=headers)
    if response.status_code == 200:
        new_version = response.json()["new_version"]
        print(f"✅ Artículo actualizado (versión {new_version})")
    else:
        print(f"❌ Error actualizando artículo: {response.text}")
    
    # 5. Ver historial de versiones
    print("🧪 Obteniendo historial de versiones...")
    response = requests.get(f"{base_url}/articles/{article_id}/versions", headers=headers)
    if response.status_code == 200:
        versions = response.json()
        print(f"✅ {versions['total_versions']} versiones encontradas")
    else:
        print(f"❌ Error obteniendo versiones: {response.text}")

if __name__ == "__main__":
    test_articles_crud()