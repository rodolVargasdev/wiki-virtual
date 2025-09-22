# from sentence_transformers import SentenceTransformer  # DESACTIVADO
# import numpy as np  # DESACTIVADO
from typing import List, Dict, Optional
import json

class EmbeddingManager:
    """
    Gestor de embeddings para búsqueda semántica (MODO DEGRADADO)
    
    Esta clase maneja:
    - Creación de embeddings (DESACTIVADO)
    - Almacenamiento en memoria
    - Búsqueda por similitud (DESACTIVADO)
    """
    
    def __init__(self):
        """Inicializar el gestor de embeddings en modo degradado"""
        print("⚠️  EmbeddingManager en MODO DEGRADADO - IA desactivada")
        
        # Modelo desactivado para arranque rápido
        self.model = None
        
        # Almacenar artículos y sus embeddings
        self.articles_data = []
        self.embeddings_matrix = None
        
        print("✅ EmbeddingManager inicializado en modo degradado")
    
    def add_article_embedding(self, article_id: str, title: str, content: str):
        """
        Agregar artículo al sistema de embeddings (MODO DEGRADADO)
        
        Args:
            article_id: ID único del artículo
            title: Título del artículo
            content: Contenido del artículo
        """
        try:
            print(f"⚠️  Modo degradado: Artículo {article_id} guardado sin embeddings")
            
            # Solo guardar datos básicos, sin embeddings
            article_data = {
                "id": article_id,
                "title": title,
                "content": content,
                "full_text": f"{title}\n\n{content}",
                "embedding": None  # Sin embedding
            }
            
            self.articles_data.append(article_data)
            
            print(f"✅ Artículo {article_id} agregado (sin embeddings)")
            
        except Exception as e:
            print(f"❌ Error agregando artículo: {str(e)}")
            raise e
    
    def _rebuild_embeddings_matrix(self):
        """
        Reconstruir matriz de embeddings (DESACTIVADO)
        """
        print("⚠️  Modo degradado: Matriz de embeddings desactivada")
        self.embeddings_matrix = None
    
    def search_similar_articles(self, query: str, k: int = 3) -> List[Dict]:
        """
        Buscar artículos similares (MODO DEGRADADO - búsqueda por texto)
        
        Args:
            query: Consulta del usuario
            k: Número de artículos a retornar
            
        Returns:
            List[Dict]: Lista de artículos encontrados por búsqueda de texto
        """
        try:
            if not self.articles_data:
                print("⚠️ No hay artículos indexados para buscar")
                return []
            
            print(f"⚠️  Modo degradado: Búsqueda por texto simple para: '{query[:50]}...'")
            
            # Búsqueda simple por texto (sin embeddings)
            query_lower = query.lower()
            results = []
            
            for article in self.articles_data:
                # Buscar en título y contenido
                title_match = query_lower in article["title"].lower()
                content_match = query_lower in article["content"].lower()
                
                if title_match or content_match:
                    article_copy = article.copy()
                    article_copy["similarity_score"] = 0.8 if title_match else 0.6  # Score fijo
                    article_copy.pop("embedding", None)  # Remover embedding si existe
                    results.append(article_copy)
            
            # Limitar resultados
            results = results[:k]
            
            print(f"✅ {len(results)} artículos encontrados (búsqueda por texto)")
            return results
            
        except Exception as e:
            print(f"❌ Error buscando artículos: {str(e)}")
            return []
    
    def get_index_stats(self) -> Dict:
        """
        Obtener estadísticas del sistema de embeddings (MODO DEGRADADO)
        
        Returns:
            Dict: Estadísticas del sistema
        """
        return {
            "total_articles": len(self.articles_data),
            "embeddings_loaded": False,  # Siempre False en modo degradado
            "model_name": "MODO_DEGRADADO",
            "search_mode": "text_search"
        }

# Instancia global del gestor de embeddings
embedding_manager = EmbeddingManager()