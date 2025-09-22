import firebase_admin
from firebase_admin import credentials, auth
import json

def check_firebase_admin():
    """Verificar qué proyecto está usando Firebase Admin"""
    
    print("🔍 Verificando configuración de Firebase Admin...")
    
    # Inicializar Firebase si no está inicializado
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate("firebase-key.json")
            firebase_admin.initialize_app(cred)
            print("✅ Firebase Admin inicializado para verificación")
        except Exception as e:
            print(f"❌ Error inicializando Firebase: {str(e)}")
            return
    
    # Verificar si Firebase está inicializado
    if firebase_admin._apps:
        # firebase_admin._apps es un diccionario, no una lista
        app_name = list(firebase_admin._apps.keys())[0]
        app = firebase_admin._apps[app_name]
        print(f"✅ Firebase Admin inicializado")
        print(f"   Proyecto: {app.project_id}")
        
        # Verificar archivo de configuración
        try:
            with open("firebase-key.json", "r") as f:
                config = json.load(f)
            print(f"✅ Archivo firebase-key.json:")
            print(f"   Proyecto: {config['project_id']}")
            
            if app.project_id == config['project_id']:
                print("✅ Configuración consistente")
            else:
                print("❌ Configuración inconsistente")
                
        except Exception as e:
            print(f"❌ Error leyendo firebase-key.json: {str(e)}")
    else:
        print("⚠️ Firebase Admin no está inicializado")
        
        # Verificar archivo de configuración
        try:
            with open("firebase-key.json", "r") as f:
                config = json.load(f)
            print(f"✅ Archivo firebase-key.json:")
            print(f"   Proyecto: {config['project_id']}")
        except Exception as e:
            print(f"❌ Error leyendo firebase-key.json: {str(e)}")

if __name__ == "__main__":
    check_firebase_admin()
    