#!/usr/bin/env python3
"""
Script de prueba simple para verificar que la aplicación funcione
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("🔄 Probando importación de módulos...")
    
    # Probar importaciones básicas
    import fastapi
    print("✅ FastAPI importado correctamente")
    
    import uvicorn
    print("✅ Uvicorn importado correctamente")
    
    import firebase_admin
    print("✅ Firebase Admin importado correctamente")
    
    # Probar importación de main
    import main
    print("✅ main.py importado correctamente")
    
    print("\n🎉 ¡Todas las importaciones exitosas!")
    print("✅ La aplicación debería funcionar correctamente")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error inesperado: {e}")
    sys.exit(1)
