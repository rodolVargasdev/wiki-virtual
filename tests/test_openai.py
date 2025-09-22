import os
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno
load_dotenv()

def test_openai_connection():
    """Probar que podemos conectarnos a OpenAI"""
    
    # Verificar que tenemos la API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No se encontró OPENAI_API_KEY en el archivo .env")
        return
    
    print(f"✅ API Key encontrada: {api_key[:10]}...")
    
    # Crear cliente de OpenAI
    client = OpenAI(api_key=api_key)
    
    try:
        # Probar con una pregunta simple
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Di 'Hola, funciono correctamente'"}
            ],
            max_tokens=50
        )
        
        answer = response.choices[0].message.content
        print(f"✅ Respuesta de OpenAI: {answer}")
        
    except Exception as e:
        print(f"❌ Error conectando con OpenAI: {str(e)}")
        print("�� Verifica que tu API key sea correcta y tengas créditos")

if __name__ == "__main__":
    test_openai_connection()