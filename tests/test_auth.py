import firebase_admin
from firebase_admin import credentials, auth
import os
from dotenv import load_dotenv
import requests 
import json 

# Cargar variables de entorno
load_dotenv()

# Inicializar Firebase Admin
def initialize_firebase():
    """Inicializar Firebase Admin SDK"""
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase-key.json")
        firebase_admin.initialize_app(cred)
        print("✅ Firebase inicializado correctamente")

# Llamar a la inicialización
initialize_firebase()

def create_test_user():
    """
    Crear un usuario de prueba en Firebase
    """
    try:
        # Crear usuario de prueba
        user = auth.create_user(
            email="test@example.com",
            password="123456",
            display_name="Usuario de Prueba"
        )
        print(f"✅ Usuario creado: {user.uid}")
        return user.uid
    except Exception as e:
        if "email already exists" in str(e):
            print("⚠️ Usuario ya existe, obteniendo UID...")
            # Obtener usuario existente
            user = auth.get_user_by_email("test@example.com")
            return user.uid
        else:
            print(f"❌ Error creando usuario: {str(e)}")
            return None

def create_admin_user():
    """
    Crear un usuario administrador en Firebase
    """
    try: 
        # Crear usuario administrador
        admin_user = auth.create_user(
            email="admin@example.com",
            password="qw12QW",
            display_name="Usuario Administrador"
        )
        print(f"✅ Usuario creado: {admin_user.uid}, email: {admin_user.email}")

        # Asignar rol de administrador
        auth.set_custom_user_claims(admin_user.uid, {"role": "admin"})
        print(f"✅ Rol de administrador asignado a {admin_user.uid}, email: {admin_user.email} y nombre: {admin_user.display_name}")

        return admin_user.uid

    except Exception as e:
        if "email already exists" in str(e):
            print("⚠️ Usuario ya existe, obteniendo UID...")
            # Obtener usuario existente
            admin_user = auth.get_user_by_email("admin@example.com")
            return admin_user.uid
        else:
            print(f"❌ Error creando usuario administrador: {str(e)}")
            return None

def get_id_token(email: str, password: str):
    """
    Obtener token de ID para un usuario (simula login del cliente)
    
    Args:
        email: Email del usuario
        password: Contraseña del usuario
    
    Returns:
        str: Token de ID válido
    """
    # Configuración de Firebase
    api_key = os.getenv("FIREBASE_API_KEY")  # Obtener de Firebase Console
    project_id = "wiki-virtual-python-20f8f"  # Obtener de Firebase Console
    
    # URL para autenticación
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    
    # Datos de la petición
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        if response.status_code == 200:
            id_token = result["idToken"]
            print(f"✅ Token de ID obtenido para {email}")
            return id_token
        else:
            print(f"❌ Error obteniendo token: {result}")
            return None
            
    except Exception as e:
        print(f"❌ Error en la petición: {str(e)}")
        return None

def test_protected_endpoint(token: str):
    """
    Probar endpoint protegido con el token
    """
    url = "http://localhost:8000/profile"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("✅ Endpoint protegido accesible")
            print(f"Respuesta: {response.json()}")
        else:
            print(f"❌ Error accediendo endpoint: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en la petición: {str(e)}")

def test_admin_endpoint(token: str):
    """
    Probar endpoint protegido para administrador
    """
    url = "http://localhost:8000/admin-only"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Respuesta: {response.json()}")

    except Exception as e:
        print(f"❌ Error en la petición: {str(e)}")

def test_authentication():
    """
    Probar el flujo completo de autenticación
    """
    print("🧪 Iniciando prueba de autenticación...")
    
    # Paso 1: Crear usuario de prueba
    uid = create_test_user()
    if not uid:
        print("❌ No se pudo crear/obtener usuario")
        return
    
    # Paso 2: Obtener token de ID
    id_token = get_id_token("test@example.com", "123456")
    if not id_token:
        print("❌ No se pudo obtener token de ID")
        return
    
    # Paso 3: Probar endpoint protegido
    test_protected_endpoint(id_token)

def test_admin_authentication():
    """
    Probar el flujo completo de autenticación para administrador
    """
    print("🧪 Iniciando prueba de autenticación para administrador...")

    # Paso 1: Crear usuario administrador
    admin_uid = create_admin_user()
    if not admin_uid:
        print("❌ No se pudo crear usuario administrador")
        return
    
    # Paso 2: Obtener token de ID para el usuario administrador
    admin_id_token = get_id_token("admin@example.com", "qw12QW")
    if not admin_id_token:
        print("❌ No se pudo obtener token de ID para administrador")
        return
    
    # Paso 3: Probar endpoint protegido para administrador
    test_admin_endpoint(admin_id_token)


if __name__ == "__main__":
    # Ejecutar prueba completa
    test_authentication()

    # Ejecutar prueba completa para administrador
    test_admin_authentication()