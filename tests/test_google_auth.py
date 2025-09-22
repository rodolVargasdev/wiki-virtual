import requests
import json
from firebase_config import google_auth_manager

def test_google_auth():
    """Probar autenticación con Google"""
    
    print("🧪 Probando autenticación con Google...")
    
    # 1. Probar verificación de dominios
    print("\n1. Probando verificación de dominios:")
    
    test_emails = [
        "usuario@tu-empresa.com",      # Debería estar autorizado
        "admin@tu-empresa.com",        # Debería estar autorizado
        "usuario@universidad.edu",     # Debería estar autorizado
        "usuario@gmail.com",           # NO debería estar autorizado
        "usuario@yahoo.com",           # NO debería estar autorizado
        "admin@tu-empresa.com",        # Email específico permitido
    ]
    
    for email in test_emails:
        status = google_auth_manager.get_authorization_status(email)
        print(f"   {email}: {'✅ Autorizado' if status['is_authorized'] else '❌ No autorizado'}")
        if not status['is_authorized']:
            print(f"      Razón: {status['reason']}")
    
    # 2. Probar agregar/remover dominios
    print("\n2. Probando gestión de dominios:")
    
    # Agregar dominio
    google_auth_manager.add_allowed_domain("nuevo-dominio.com")
    
    # Verificar que se agregó
    status = google_auth_manager.get_authorization_status("test@nuevo-dominio.com")
    print(f"   test@nuevo-dominio.com: {'✅ Autorizado' if status['is_authorized'] else '❌ No autorizado'}")
    
    # Remover dominio
    google_auth_manager.remove_allowed_domain("nuevo-dominio.com")
    
    # Verificar que se removió
    status = google_auth_manager.get_authorization_status("test@nuevo-dominio.com")
    print(f"   test@nuevo-dominio.com (después de remover): {'✅ Autorizado' if status['is_authorized'] else '❌ No autorizado'}")
    
    # 3. Probar agregar/remover emails
    print("\n3. Probando gestión de emails:")
    
    # Agregar email
    google_auth_manager.add_allowed_email("nuevo@cualquier-dominio.com")
    
    # Verificar que se agregó
    status = google_auth_manager.get_authorization_status("nuevo@cualquier-dominio.com")
    print(f"   nuevo@cualquier-dominio.com: {'✅ Autorizado' if status['is_authorized'] else '❌ No autorizado'}")
    
    # Remover email
    google_auth_manager.remove_allowed_email("nuevo@cualquier-dominio.com")
    
    # Verificar que se removió
    status = google_auth_manager.get_authorization_status("nuevo@cualquier-dominio.com")
    print(f"   nuevo@cualquier-dominio.com (después de remover): {'✅ Autorizado' if status['is_authorized'] else '❌ No autorizado'}")
    
    print("\n✅ Test de autenticación con Google completado!")

if __name__ == "__main__":
    test_google_auth()