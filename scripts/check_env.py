import os
from dotenv import load_dotenv

def check_env_variables():
    """Verificar que las variables de entorno se cargan correctamente"""
    
    print("🔍 Verificando variables de entorno...")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar variables importantes
    variables = [
        "FIREBASE_PROJECT_ID",
        "FIREBASE_API_KEY", 
        "ALLOWED_EMAILS",
        "GEMINI_API_KEY",
        "ENVIRONMENT"
    ]
    
    for var in variables:
        value = os.getenv(var)
        if value:
            if var == "FIREBASE_API_KEY":
                print(f"✅ {var}: {value[:20]}...")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: No encontrada")
    
    # Verificar proyecto específico
    project_id = os.getenv("FIREBASE_PROJECT_ID")
    if project_id == "wiki-virtual-python-20f8f":
        print("✅ Proyecto Firebase correcto")
    else:
        print(f"❌ Proyecto Firebase incorrecto: {project_id}")
    
    # Verificar emails permitidos
    allowed_emails = os.getenv("ALLOWED_EMAILS", "").split(",")
    if "admin@example.com" in allowed_emails:
        print("✅ admin@example.com está en la lista de emails permitidos")
    else:
        print("❌ admin@example.com NO está en la lista de emails permitidos")

if __name__ == "__main__":
    check_env_variables()