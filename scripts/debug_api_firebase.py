#!/usr/bin/env python3
"""
Script para debuggear la configuración de Firebase en la API
"""

import os
import sys
sys.path.append('.')

# Simular el proceso de inicialización de la API
print("🔍 Debuggeando configuración de Firebase en la API...")

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

print(f"📁 Directorio actual: {os.getcwd()}")
print(f"📁 Archivo firebase-key.json existe: {os.path.exists('firebase-key.json')}")

# Verificar variables de entorno
print(f"🔑 FIREBASE_PROJECT_ID: {os.getenv('FIREBASE_PROJECT_ID')}")

# Importar y verificar firebase_config
try:
    from firebase_config import initialize_firebase
    print("✅ firebase_config importado correctamente")
    
    # Inicializar Firebase
    initialize_firebase()
    
    # Verificar configuración
    import firebase_admin
    if firebase_admin._apps:
        app_name = list(firebase_admin._apps.keys())[0]
        app = firebase_admin._apps[app_name]
        print(f"✅ Firebase Admin inicializado en API")
        print(f"📄 Proyecto: {app.project_id}")
    else:
        print("❌ Firebase Admin no inicializado")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
