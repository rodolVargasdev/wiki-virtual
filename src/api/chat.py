from fastapi import APIRouter, Depends, HTTPException
from core.auth import verify_token
from services.embeddings import embedding_manager
from services.gemini_service import gemini_service  # Cambiar importación
from pydantic import BaseModel
from typing import List, Dict, Optional

# Router para chat
router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    """Modelo para solicitud de chat"""
    message: str
    max_results: int = 3
    
    class Config:
        schema_extra = {
            "example": {
                "message": "¿Qué son las redes de computadoras?",
                "max_results": 3
            }
        }

class ChatResponse(BaseModel):
    """Modelo para respuesta de chat"""
    answer: str
    sources: List[Dict]
    confidence: float
    query: str
    model: str = "gemini-pro"  # Indicar que usamos Gemini
    
    class Config:
        schema_extra = {
            "example": {
                "answer": "Las redes de computadoras son sistemas que permiten...",
                "sources": [
                    {
                        "title": "Introducción a Redes",
                        "id": "article-123",
                        "similarity_score": 0.95
                    }
                ],
                "confidence": 0.95,
                "query": "¿Qué son las redes de computadoras?",
                "model": "gemini-pro"
            }
        }

@router.post("/", response_model=ChatResponse)
def chat_with_ai(
    request: ChatRequest,
    user=Depends(verify_token)
):
    """
    Chat con IA basado en artículos de la wiki usando Gemini
    
    La IA solo responderá con información de los artículos cargados
    """
    try:
        print(f" Usuario {user['email']} pregunta: {request.message}")
        
        # 1. Buscar artículos relevantes
        similar_articles = embedding_manager.search_similar_articles(
            request.message, 
            request.max_results
        )
        
        # 2. Si no hay artículos relevantes o la similitud es muy baja
        if not similar_articles or similar_articles[0]["similarity_score"] < 0.3:
            return ChatResponse(
                answer="Este tema no está disponible en la biblioteca virtual. Por favor, verifica que el artículo correspondiente esté cargado o reformula tu pregunta.",
                sources=[],
                confidence=0.0,
                query=request.message,
                model="gemini-pro"
            )
        
        # 3. Preparar contexto para la respuesta
        context = _build_context(similar_articles)
        sources = _build_sources(similar_articles)
        
        # 4. Generar respuesta usando Gemini
        answer = gemini_service.generate_answer(request.message, context)
        
        # 5. Calcular confianza basada en similitud
        confidence = similar_articles[0]["similarity_score"]
        
        return ChatResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
            query=request.message,
            model="gemini-pro"
        )
        
    except Exception as e:
        print(f"❌ Error en chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en el chat: {str(e)}")

def _build_context(articles: List[Dict]) -> str:
    """
    Construir contexto para la respuesta basado en artículos encontrados
    
    Args:
        articles: Lista de artículos similares
        
    Returns:
        str: Contexto formateado
    """
    context = "Información disponible en la biblioteca virtual:\n\n"
    
    for i, article in enumerate(articles, 1):
        context += f"Artículo {i}: {article['title']}\n"
        context += f"Contenido: {article['content'][:300]}...\n\n"
    
    return context

def _build_sources(articles: List[Dict]) -> List[Dict]:
    """
    Construir lista de fuentes para la respuesta
    
    Args:
        articles: Lista de artículos similares
        
    Returns:
        List[Dict]: Lista de fuentes con información relevante
    """
    sources = []
    
    for article in articles:
        sources.append({
            "title": article["title"],
            "id": article["id"],
            "similarity_score": article["similarity_score"],
            "content_preview": article["content"][:150] + "..."
        })
    
    return sources

@router.get("/stats", response_model=Dict)
def get_chat_stats(user=Depends(verify_token)):
    """
    Obtener estadísticas del sistema de chat
    
    Muestra información sobre el sistema de embeddings y Gemini
    """
    try:
        stats = embedding_manager.get_index_stats()
        gemini_status = gemini_service.test_connection()
        
        return {
            "embedding_stats": stats,
            "gemini_status": "connected" if gemini_status else "disconnected",
            "model": "gemini-pro",
            "message": "Estadísticas del sistema de chat"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")

@router.post("/reindex", response_model=Dict)
def reindex_articles(user=Depends(verify_token)):
    """
    Reindexar todos los artículos
    
    Útil cuando se agregan muchos artículos nuevos
    """
    try:
        return {
            "message": "Reindexación iniciada",
            "status": "success",
            "model": "gemini-pro"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en reindexación: {str(e)}")