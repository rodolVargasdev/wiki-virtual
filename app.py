import os
from fastapi import FastAPI

# Crear instancia de FastAPI
app = FastAPI(
    title="Wiki Virtual API",
    description="API para wiki educativa con FastAPI",
    version="1.0.0"
)

PORT = int(os.environ.get("PORT", 8080))

# Endpoint raiz
@app.get("/")
def root():
    return {
        "message": "¡Hola! Esta es tu API con FastAPI",
        "status": "running",
        "version": "1.0.0",
        "port": PORT,
        "environment": os.environ.get("ENVIRONMENT", "development")
    }

# Endpoint de salud
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "API funcionando correctamente",
        "port": PORT,
        "environment": os.environ.get("ENVIRONMENT", "development")
    }

# Endpoint de información del proyecto
@app.get("/info")
def project_info():
    return {
        "project": "Wiki Virtual",
        "description": "Sistema educativo con FastAPI",
        "technologies": ["FastAPI", "Python"],
        "author": "JOSE-"
    }
