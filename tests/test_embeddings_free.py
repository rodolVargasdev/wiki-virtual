from sentence_transformers import SentenceTransformer
import numpy as np

def test_free_embeddings():
    """Probar embeddings gratuitos con sentence-transformers"""
    
    print("🔄 Cargando modelo de embeddings...")
    
    # Cargar modelo (se descarga la primera vez)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("✅ Modelo cargado correctamente")
    
    # Textos de prueba
    texts = [
        "Las redes de computadoras son sistemas de comunicación",
        "Los gatos son animales domésticos",
        "La programación es el arte de resolver problemas",
        "Las redes informáticas permiten compartir datos"
    ]
    
    print("\n🧪 Creando embeddings...")
    
    # Crear embeddings
    embeddings = model.encode(texts)
    
    print(f"✅ Embeddings creados: {embeddings.shape}")
    print(f"   - Número de textos: {embeddings.shape[0]}")
    print(f"   - Dimensión de cada embedding: {embeddings.shape[1]}")
    
    # Calcular similitud entre textos
    print("\n�� Calculando similitudes...")
    
    # Texto de consulta
    query = "¿Qué son las redes de computadoras?"
    query_embedding = model.encode([query])
    
    # Calcular similitudes
    similarities = np.dot(embeddings, query_embedding.T).flatten()
    
    print(f"Consulta: '{query}'")
    print("\nSimilitudes con cada texto:")
    
    for i, (text, similarity) in enumerate(zip(texts, similarities)):
        print(f"  {i+1}. Similitud: {similarity:.3f} - '{text[:50]}...'")
    
    # Encontrar el texto más similar
    most_similar_idx = np.argmax(similarities)
    print(f"\n✅ Texto más similar: '{texts[most_similar_idx]}'")
    print(f"   Similitud: {similarities[most_similar_idx]:.3f}")

if __name__ == "__main__":
    test_free_embeddings()