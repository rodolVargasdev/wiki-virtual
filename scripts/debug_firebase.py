#!/usr/bin/env python3
"""
Script para debuggear la configuración de Firebase
"""

import firebase_admin
from firebase_admin import credentials
import json
import os

def debug_firebase():
    print("🔍 Debuggeando configuración de Firebase...")
    
    # Verificar archivo actual
    print(f"📁 Directorio actual: {os.getcwd()}")
    print(f"📁 Archivo firebase-key.json existe: {os.path.exists('firebase-key.json')}")
    
    if os.path.exists('firebase-key.json'):
        with open('firebase-key.json', 'r') as f:
            config = json.load(f)
        print(f"📄 Proyecto en firebase-key.json: {config['project_id']}")
    
    # Verificar si Firebase está inicializado
    if firebase_admin._apps:
        print("✅ Firebase Admin está inicializado")
        app_name = list(firebase_admin._apps.keys())[0]
        app = firebase_admin._apps[app_name]
        print(f"📄 Proyecto en Firebase Admin: {app.project_id}")
        
        # Verificar credenciales
        if hasattr(app, '_credential') and app._credential:
            print(f"🔑 Credenciales cargadas: {type(app._credential)}")
    else:
        print("⚠️ Firebase Admin no está inicializado")
        
        # Intentar inicializar
        try:
            cred = credentials.Certificate("firebase-key.json")
            app = firebase_admin.initialize_app(cred)
            print(f"✅ Firebase Admin inicializado con proyecto: {app.project_id}")
        except Exception as e:
            print(f"❌ Error inicializando Firebase: {str(e)}")

if __name__ == "__main__":
    debug_firebase()
