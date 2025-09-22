from services.embeddings import embedding_manager
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from models.models import ArticleCreate, ArticleUpdate, ArticleResponse, ArticleListResponse
from utils.firestore_utils import FirestoreManager
from core.auth import verify_token, require_role
from datetime import datetime

# Router para artículos
router = APIRouter(prefix="/articles", tags=["articles"])

@router.post("/", response_model=dict)
def create_article(
    article: ArticleCreate,
    user=Depends(require_role("admin"))
):
    """
    Crear un nuevo artículo
    
    Solo los administradores pueden crear artículos
    """
    try:
        # Convertir a diccionario y agregar autor
        article_data = article.dict()
        article_data["author"] = user["uid"]
        
        # Crear artículo
        article_id = FirestoreManager.create_article(article_data)
        
        # Agregar al sistema de embeddings
        embedding_manager.add_article_embedding(
            article_id, 
            article.title, 
            article.content
        )
        
        return {
            "message": "Artículo creado exitosamente",
            "article_id": article_id,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando artículo: {str(e)}")


@router.get("/", response_model=ArticleListResponse)
def list_articles(
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de artículos"),
    page: int = Query(1, ge=1, description="Página actual"),
    user=Depends(verify_token)
):
    """
    Listar artículos con filtros opcionales
    
    Todos los usuarios autenticados pueden listar artículos
    """
    try:
        # Obtener artículos
        articles = FirestoreManager.list_articles(category, limit, page)
        
        return ArticleListResponse(
            articles=articles,
            total=len(articles),
            page=page,
            limit=limit
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando artículos: {str(e)}")

@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(
    article_id: str,
    user=Depends(verify_token)
):
    """
    Obtener un artículo específico por ID
    
    Todos los usuarios autenticados pueden ver artículos
    """
    try:
        article = FirestoreManager.get_article(article_id)
        
        if not article:
            raise HTTPException(status_code=404, detail="Artículo no encontrado")
        
        return ArticleResponse(**article)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo artículo: {str(e)}")

@router.put("/{article_id}", response_model=dict)
def update_article(
    article_id: str,
    article_update: ArticleUpdate,
    user=Depends(require_role("admin"))
):
    """
    Actualizar un artículo existente
    
    Solo los administradores pueden actualizar artículos
    Se crea una nueva versión automáticamente
    """
    try:
        # Verificar que el artículo existe
        existing_article = FirestoreManager.get_article(article_id)
        if not existing_article:
            raise HTTPException(status_code=404, detail="Artículo no encontrado")
        
        # Filtrar campos None
        update_data = {k: v for k, v in article_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay datos para actualizar")
        
        # Actualizar artículo
        new_version = FirestoreManager.update_article(article_id, update_data)
        
        # Actualizar en sistema de embeddings
        if "title" in update_data or "content" in update_data:
            # Obtener datos actualizados
            updated_article = FirestoreManager.get_article(article_id)
            embedding_manager.add_article_embedding(
                article_id,
                updated_article["title"],
                updated_article["content"]
            )
        
        return {
            "message": "Artículo actualizado exitosamente",
            "article_id": article_id,
            "new_version": new_version,
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando artículo: {str(e)}")

@router.delete("/{article_id}", response_model=dict)
def delete_article(
    article_id: str,
    user=Depends(require_role("admin"))
):
    """
    Eliminar un artículo (soft delete)
    
    Solo los administradores pueden eliminar artículos
    El artículo se archiva, no se borra permanentemente
    """
    try:
        # Verificar que el artículo existe
        existing_article = FirestoreManager.get_article(article_id)
        if not existing_article:
            raise HTTPException(status_code=404, detail="Artículo no encontrado")
        
        # Eliminar artículo (soft delete)
        FirestoreManager.delete_article(article_id)
        
        return {
            "message": "Artículo eliminado exitosamente",
            "article_id": article_id,
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando artículo: {str(e)}")

@router.get("/{article_id}/versions", response_model=dict)
def get_article_versions(
    article_id: str,
    user=Depends(verify_token)
):
    """
    Obtener historial de versiones de un artículo
    
    Todos los usuarios autenticados pueden ver el historial
    """
    try:
        # Verificar que el artículo existe
        existing_article = FirestoreManager.get_article(article_id)
        if not existing_article:
            raise HTTPException(status_code=404, detail="Artículo no encontrado")
        
        # Obtener versiones
        versions = FirestoreManager.get_article_versions(article_id)
        
        return {
            "article_id": article_id,
            "versions": versions,
            "total_versions": len(versions)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo versiones: {str(e)}")