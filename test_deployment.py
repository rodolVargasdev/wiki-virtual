#!/usr/bin/env python3
"""
Script de prueba completo para verificar que la aplicación esté lista para despliegue
"""

import sys
import os
import subprocess
import time
import requests

def test_imports():
    """Probar importaciones de la aplicación"""
    print("🔄 Probando importaciones...")
    
    # Agregar src al path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        import main
        print("✅ main.py importado correctamente")
        print(f"✅ FastAPI app: {main.app.title}")
        print(f"✅ Puerto configurado: {main.PORT}")
        return True
    except Exception as e:
        print(f"❌ Error importando main.py: {e}")
        return False

def test_docker_build():
    """Probar build de Docker"""
    print("🔄 Probando build de Docker...")
    
    try:
        result = subprocess.run(
            ["docker", "build", "-t", "test-wiki-virtual", "."],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print("✅ Docker build exitoso")
            return True
        else:
            print(f"❌ Docker build falló: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Docker build timeout")
        return False
    except FileNotFoundError:
        print("❌ Docker no encontrado")
        return False

def test_docker_run():
    """Probar ejecución de Docker"""
    print("🔄 Probando ejecución de Docker...")
    
    try:
        # Ejecutar contenedor
        result = subprocess.run(
            ["docker", "run", "-d", "-p", "8080:8080", "--name", "test-container", "test-wiki-virtual"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ Error ejecutando contenedor: {result.stderr}")
            return False
        
        # Esperar a que la aplicación inicie
        print("⏳ Esperando que la aplicación inicie...")
        time.sleep(15)
        
        # Probar endpoint de salud
        try:
            response = requests.get("http://localhost:8080/health", timeout=10)
            if response.status_code == 200:
                print("✅ Aplicación responde correctamente")
                print(f"✅ Respuesta: {response.json()}")
                return True
            else:
                print(f"❌ Aplicación responde con código: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Error conectando a la aplicación: {e}")
            return False
        finally:
            # Limpiar contenedor
            subprocess.run(["docker", "stop", "test-container"], capture_output=True)
            subprocess.run(["docker", "rm", "test-container"], capture_output=True)
    
    except Exception as e:
        print(f"❌ Error en prueba de Docker: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("🚀 Iniciando pruebas de despliegue...")
    print("=" * 50)
    
    tests = [
        ("Importaciones", test_imports),
        ("Docker Build", test_docker_build),
        ("Docker Run", test_docker_run)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        result = test_func()
        results.append((test_name, result))
        print("-" * 30)
    
    print("\n📊 Resultados:")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("🎉 ¡Todas las pruebas pasaron! La aplicación está lista para despliegue.")
        return 0
    else:
        print("❌ Algunas pruebas fallaron. Revisa los errores antes del despliegue.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
