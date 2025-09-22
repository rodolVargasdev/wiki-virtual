import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Depends, Header
from typing import Optional
import os
import json
from .firebase_config import google_auth_manager

def initialize_firebase():
    """ Inicializar Firebase Admin """
    if not firebase_admin._apps:
        try:
            service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
            if not service_account_json:
                raise ValueError("FIREBASE_SERVICE_ACCOUNT_JSON not set")
            cred_dict = json.loads(service_account_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin inicializado correctamente")
        except Exception as e:
            print(f"❌ Error inicializando Firebase in auth: {str(e)}")
            # Don't raise; degraded mode

# No auto-init; called from main.py

def verify_token(authorization: Optional[str] = Header(None)):
    """
    Verificar el token de Google en cada request
    
    Args:
        authorization: Header con formato "Bearer <token>"
    
    Returns:
        dict: Información del usuario autenticado
    
    Raises:
        HTTPException: Si el token es inválido o usuario no autorizado
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token de autorización requerido"
        )
    
    try:
        # Extraer token del header "Bearer <token>"
        token = authorization.split(" ")[1]
        
        # Verificar token con Google Auth Manager
        user_info = google_auth_manager.verify_google_token(token)
        
        print(f"✅ Usuario autenticado: {user_info['email']}")
        return user_info
        
    except ValueError as e:
        # Usuario no autorizado
        raise HTTPException(
            status_code=403,
            detail=f"Acceso denegado: {str(e)}"
        )
    except Exception as e:
        # Token inválido
        print(f"❌ Error de autenticación: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail=f"Token inválido: {str(e)}"
        )
    
def get_user_role(uid: str) -> str:
    """
    Obtiene el rol del usuario desde Firebase Custom Claims

    Args:
        uid: ID del usuario
    
    Returns:
        str: Rol del usuario
    
    Raises:
        HTTPException: Si el usuario no existe o no tiene un rol
    """

    try:
        if not firebase_admin._apps:
            print("Firebase not initialized; default role 'user'")
            return 'user'
        user = auth.get_user(uid)
        # Por defecto, todos los usuarios son 'user'
        return user.custom_claims.get('role', 'user')

    except Exception as e:
        print(f"Error obteniendo rol: {str(e)}")
        return 'user'

def require_role(required_role: str):
    """
    Decorador para requerir un rol específico

    Args:
        required_role: Rol requerido ('admin', 'user', etc.)

    Returns:
        function: Decorador que verifica el rol del usuario
    """

    def role_checker(user=Depends(verify_token)):
        user_role = get_user_role(user['uid'])
        
        # Los admins pueden acceder a todo
        if user_role != required_role and user_role != 'admin':
            raise HTTPException(
                status_code=403,
                detail=f"Permisos insuficientes. Rol requerido: {required_role}"
            )
        
        print(f"✅ Acceso concedido para rol: {user_role}")
        return user
    
    return role_checker

