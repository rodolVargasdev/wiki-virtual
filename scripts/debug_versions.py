import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar Firebase Admin
def initialize_firebase():
    """Inicializar Firebase Admin SDK"""
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase-key.json")
        firebase_admin.initialize_app(cred)
        print("✅ Firebase inicializado correctamente")

# Llamar a la inicialización
initialize_firebase()

# Cliente de Firestore
db = firestore.client()

def debug_versions_query(article_id: str):
    """
    Función de debug para probar la consulta de versiones
    """
    print(f"🔍 Debuggeando consulta para artículo: {article_id}")
    
    try:
        # Primero, verificar si existen versiones
        print("1. Verificando si existen versiones...")
        all_versions = db.collection("article_versions").stream()
        version_count = 0
        for doc in all_versions:
            version_count += 1
            data = doc.to_dict()
            print(f"   - Versión encontrada: article_id={data.get('article_id')}, version={data.get('version')}")
        
        print(f"   Total de versiones en la colección: {version_count}")
        
        # Segundo, probar consulta simple
        print("2. Probando consulta simple (sin order_by)...")
        simple_query = db.collection("article_versions").where("article_id", "==", article_id).stream()
        simple_results = []
        for doc in simple_query:
            data = doc.to_dict()
            simple_results.append(data)
            print(f"   - Encontrado: version={data.get('version')}")
        
        print(f"   Resultados de consulta simple: {len(simple_results)}")
        
        # Tercero, probar consulta con order_by
        print("3. Probando consulta con order_by...")
        try:
            order_query = db.collection("article_versions")\
                .where("article_id", "==", article_id)\
                .order_by("version", direction=firestore.Query.DESCENDING)\
                .stream()
            
            order_results = []
            for doc in order_query:
                data = doc.to_dict()
                order_results.append(data)
                print(f"   - Encontrado: version={data.get('version')}")
            
            print(f"   Resultados de consulta con order_by: {len(order_results)}")
            print("✅ Consulta con order_by funcionó correctamente")
            
        except Exception as order_error:
            print(f"❌ Error en consulta con order_by: {str(order_error)}")
            print(f"   Tipo de error: {type(order_error).__name__}")
            
            # Información adicional sobre el error
            if "index" in str(order_error).lower():
                print("   💡 Este error sugiere un problema con el índice compuesto")
                print("   💡 Verifica que el índice incluya: article_id (Ascending), version (Descending)")
            elif "permission" in str(order_error).lower():
                print("   💡 Este error sugiere un problema de permisos")
            else:
                print("   💡 Error inesperado, revisa la configuración de Firestore")
        
    except Exception as e:
        print(f"❌ Error general: {str(e)}")
        print(f"   Tipo de error: {type(e).__name__}")

if __name__ == "__main__":
    # Usar el ID del artículo que se creó en la prueba anterior
    article_id = "6000c829-995e-48e6-8105-4ed914c5de12"  # Reemplaza con el ID real
    debug_versions_query(article_id)
