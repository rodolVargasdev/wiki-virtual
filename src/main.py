import os
from fastapi import FastAPI, Depends
import firebase_admin
from core.auth import verify_token, require_role
from api.articles import router as articles_router
from api.chat import router as chat_router
from core.firebase_config import initialize_firebase  # Agregar esta línea

# Inicializar Firebase Admin con manejo de errores
try:
    initialize_firebase()
    print("✅ Firebase inicializado en main.py")
except Exception as e:
    print(f"⚠️  Firebase no disponible: {str(e)}")
    print("App continuará en modo degradado (sin auth/Firestore)")

PORT = int(os.environ.get("PORT", 8080))

# Crear instancia de FastAPI
app = FastAPI(
    title="Wiki Virtual API",
    description="API para wiki educativa con FastAPI + Firebase + RAG",
    version="1.0.0"
)

# Incluir routers
app.include_router(articles_router)
app.include_router(chat_router)

# Endpoint raiz
@app.get("/")
def root():
    return {
        "message": "¡Hola! Esta es tu primera API con FastAPI",
        "status": "running",
        "version": "1.0.0",
        "port": PORT,
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "endpoints": {
            "articles": "/articles",
            "chat": "/chat",
            "profile": "/profile",
            "admin": "/admin-only",
            "docs": "/docs"
        }
    }

# Endpoint de salud
@app.get("/health")
def health_check():
    firebase_status = "available" if firebase_admin._apps else "degraded"
    return {
        "status": "healthy",
        "message": "API funcionando correctamente",
        "port": PORT,
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "firebase": firebase_status
    }

# Endpoint de información del proyecto
@app.get("/info")
def project_info():
    return {
        "project": "Wiki Virtual",
        "description": "Sistema educativo con FastAPI, Firebase y RAG",
        "technologies": ["FastAPI", "Firebase", "RAG", "Python"],
        "author": "JOSE-"
    }

# Endpoint de información personal
personal_info_fito = {
    "name": "Fito",
    "age": 20,
    "tecnologies": ["Python", "FastAPI", "Firebase", "RAG"],
    "projects": ["Wiki Virtual", "FastAPI", "Firebase", "RAG"],
    "objective": "Learn about FastAPI, Firebase and RAG"
}

@app.get("/personal-info")
def personal_info():
    return personal_info_fito

@app.get("/profile")
def get_profile(user=Depends(verify_token)):
    """
    Obtener perfil del usuario autenticado

    Este endpoint requiere un token váliudo de Firebase Auth
    """

    return {
        "uid": user["uid"],
        "email": user.get("email"),
        "name": user.get("name"),
        "message": "¡Bienvenido! Estás autenticado correctamente"
    }

# Endpoint solo para administradores
@app.get("/admin-only")
def admin_endpoint(user=Depends(require_role("admin"))):
    """
    Endpoint solo para administradores

    Este endpoint requiere un token válido de Firebase Auth y ser administrador
    """
    return {
        "message": "Acceso de administrador concedido",
        "user": user["email"]
    }