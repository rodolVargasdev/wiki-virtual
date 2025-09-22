import firebase_admin
from firebase_admin import credentials, auth
import os
import json

def initialize_firebase():
    """Inicializar Firebase Admin SDK"""
    if not firebase_admin._apps:
        try:
            service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
            if not service_account_json:
                raise ValueError("FIREBASE_SERVICE_ACCOUNT_JSON environment variable is not set")
            
            # Parse the JSON string
            cred_dict = json.loads(service_account_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase inicializado correctamente con env vars")
        except Exception as e:
            print(f"❌ Error inicializando Firebase: {str(e)}")
            print("⚠️  App continuará sin Firebase (degraded mode)")
            # Don't raise; let app start for partial functionality

# NO llamar automáticamente - se llamará desde main.py
# initialize_firebase()  # COMENTAR ESTA LÍNEA

class GoogleAuthManager:
    """Gestor de autenticación con Google"""
    
    def __init__(self):
        self.allowed_domains = os.getenv("ALLOWED_DOMAINS", "").split(",")
        self.allowed_emails = os.getenv("ALLOWED_EMAILS", "").split(",")
        
        print(f"✅ Dominios permitidos: {self.allowed_domains}")
        print(f"✅ Emails permitidos: {self.allowed_emails}")
    
    def verify_google_token(self, id_token: str) -> dict:
        """
        Verificar token de Google y aplicar restricciones
        
        Args:
            id_token: Token de ID de Google
            
        Returns:
            dict: Información del usuario si está autorizado
            
        Raises:
            HTTPException: Si el usuario no está autorizado
        """
        try:
            # Verificar token con Firebase
            decoded_token = auth.verify_id_token(id_token)
            
            # Extraer información del usuario
            user_info = {
                "uid": decoded_token["uid"],
                "email": decoded_token.get("email"),
                "name": decoded_token.get("name"),
                "picture": decoded_token.get("picture"),
                "email_verified": decoded_token.get("email_verified", False)
            }
            
            # Verificar restricciones
            if not self._is_user_authorized(user_info["email"]):
                raise ValueError(f"Usuario {user_info['email']} no está autorizado")
            
            print(f"✅ Usuario autorizado: {user_info['email']}")
            return user_info
            
        except Exception as e:
            print(f"❌ Error verificando token: {str(e)}")
            raise e
    
    def _is_user_authorized(self, email: str) -> bool:
        """
        Verificar si el usuario está autorizado
        
        Args:
            email: Email del usuario
            
        Returns:
            bool: True si está autorizado, False en caso contrario
        """
        if not email:
            return False
        
        # Verificar email específico
        if email in self.allowed_emails:
            return True
        
        # Verificar dominio
        domain = email.split("@")[-1]
        if domain in self.allowed_domains:
            return True
        
        return False
    
    def add_allowed_domain(self, domain: str):
        """Agregar dominio permitido"""
        if domain not in self.allowed_domains:
            self.allowed_domains.append(domain)
            print(f"✅ Dominio agregado: {domain}")
    
    def add_allowed_email(self, email: str):
        """Agregar email permitido"""
        if email not in self.allowed_emails:
            self.allowed_emails.append(email)
            print(f"✅ Email agregado: {email}")
    
    def remove_allowed_domain(self, domain: str):
        """Remover dominio permitido"""
        if domain in self.allowed_domains:
            self.allowed_domains.remove(domain)
            print(f"✅ Dominio removido: {domain}")
    
    def remove_allowed_email(self, email: str):
        """Remover email permitido"""
        if email in self.allowed_emails:
            self.allowed_emails.remove(email)
            print(f"✅ Email removido: {email}")
    
    def get_authorization_status(self, email: str) -> dict:
        """
        Obtener estado de autorización de un usuario
        
        Args:
            email: Email del usuario
            
        Returns:
            dict: Estado de autorización
        """
        is_authorized = self._is_user_authorized(email)
        
        return {
            "email": email,
            "is_authorized": is_authorized,
            "reason": self._get_authorization_reason(email) if not is_authorized else "Usuario autorizado"
        }
    
    def _get_authorization_reason(self, email: str) -> str:
        """Obtener razón por la cual el usuario no está autorizado"""
        if not email:
            return "Email no proporcionado"
        
        domain = email.split("@")[-1]
        
        if domain not in self.allowed_domains:
            return f"Dominio '{domain}' no está en la lista de dominios permitidos"
        
        if email not in self.allowed_emails:
            return f"Email '{email}' no está en la lista de emails permitidos"
        
        return "Usuario no autorizado"

# Instancia global del gestor de autenticación
google_auth_manager = GoogleAuthManager()