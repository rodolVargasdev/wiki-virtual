import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def regenerate_token():
    """Regenerar token para el proyecto correcto"""
    
    print("🔄 Regenerando token para proyecto correcto...")
    
    # Configuración de Firebase
    api_key = os.getenv("FIREBASE_API_KEY")
    project_id = os.getenv("FIREBASE_PROJECT_ID")
    
    print(f"✅ Usando API key: {api_key[:20]}...")
    print(f"✅ Usando proyecto: {project_id}")
    
    # URL para autenticación
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    
    # Datos de la petición
    data = {
        "email": "admin@example.com",
        "password": "qw12QW",
        "returnSecureToken": True
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        if response.status_code == 200:
            id_token = result["idToken"]
            print(f"✅ Token regenerado exitosamente")
            print(f"   Token: {id_token[:50]}...")
            
            # Verificar que el token es para el proyecto correcto
            import base64
            import json
            
            # Decodificar el token para verificar el audience
            parts = id_token.split('.')
            payload = json.loads(base64.b64decode(parts[1] + '==').decode('utf-8'))
            
            print(f"   Audience (aud): {payload.get('aud')}")
            print(f"   Proyecto esperado: {project_id}")
            
            if payload.get('aud') == project_id:
                print("✅ Token es para el proyecto correcto")
                return id_token
            else:
                print("❌ Token es para proyecto incorrecto")
                return None
                
        else:
            print(f"❌ Error regenerando token: {result}")
            return None
            
    except Exception as e:
        print(f"❌ Error en la petición: {str(e)}")
        return None

if __name__ == "__main__":
    token = regenerate_token()
    if token:
        print(f"\n🎉 Token regenerado correctamente!")
        print(f"   Usa este token para probar: {token[:50]}...")
    else:
        print(f"\n❌ No se pudo regenerar el token")