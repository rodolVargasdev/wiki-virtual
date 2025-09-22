from firebase_admin import firestore
from datetime import datetime
from typing import Dict, List, Optional
import uuid

# Cliente de Firestore (lazy initialization)
db = None

def get_db():
    """Obtener cliente de Firestore con lazy initialization"""
    global db
    if db is None:
        try:
            db = firestore.client()
        except Exception as e:
            print(f"⚠️  Firestore no disponible: {str(e)}")
            return None
    return db

class FirestoreManager:
    """
        Clase para manejar operaciones de Firestore    
    """
    @staticmethod
    def create_article(article_data: Dict) -> str:
        """
            Crear un nuevo artículo en Firestore

            Args:
                article_data: Datos del artículo

            Returns:
                str: ID del artículo creado
        """

        try:
            # Generar ID único
            article_id = str(uuid.uuid4())

            # Agregar metadatos
            article_data.update({
                "id": article_id,
                "version" : 1,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "status": "published"
            })

            # Guardar en Firestore
            db_client = get_db()
            if db_client is None:
                raise Exception("Firestore no disponible")
            db_client.collection("articles").document(article_id).set(article_data)

            # Crear versión inicial
            FirestoreManager.create_article_version(article_id, article_data, 1)

            print(f"✅ Artículo creado: {article_id}")
            return article_id
        
        except Exception as e:
            print(f"❌ Error al crear artículo: {str(e)}")
            return e

    @staticmethod
    def get_article(article_id: str) -> Optional[Dict]:
        """
            Obtener un artículo por su ID
        
            Args:
                article_id: ID del artículo

            Returns:
                Optional[Dict]: Datos del artículo o None si no existe
        """
        try: 
            db_client = get_db()
            if db_client is None:
                raise Exception("Firestore no disponible")
            doc = db_client.collection("articles").document(article_id).get()

            if doc.exists:
                return {"id": doc.id, **doc.to_dict()}
            else:
                return None
            
        except Exception as e:
            print(f"❌ Error al obtener artículo: {str(e)}")
            raise e
        
    @staticmethod
    def list_articles(
        category: Optional[str] = None,
        limit: int = 10,
        page: int = 1
    ) -> List[Dict]:
        """
            Listar artículos con filtros

            Args:
                category: Categoría del artículo
                limit: Límite de artículos por página
                page: Número de página

            Returns:
                List[Dict]: Lista de artículos
        """
        try: 
            # Construir consulta
            db_client = get_db()
            if db_client is None:
                raise Exception("Firestore no disponible")
            query = db_client.collection("articles").where("visibility", "==", "public")

            if category:
                query = query.where("category", "==", category)

            # Aplicar paginación
            offset = (page - 1) * limit
            query = query.offset(offset).limit(limit)

            # Ejecutar consulta
            docs = query.stream()

            articles = []
            for doc in docs:
                articles.append({"id": doc.id, **doc.to_dict()})
            
            print(f"✅ {len(articles)} artículos encontrados")
            return articles

        except Exception as e:
            print(f"❌ Error al listar artículos: {str(e)}")
            raise e
        
    @staticmethod
    def update_article(article_id: str, update_data: Dict) -> int:
        """
            Actualizar un artículo  (crea nueva versión)

            Args: 
                article_id: ID del artículo
                update_data: Datos actualizados
            
            Returns:
                int: Número de versión actualizada
        """
        try:
            # Obtener artículo actual
            db_client = get_db()
            if db_client is None:
                raise Exception("Firestore no disponible")
            doc_ref = db_client.collection("articles").document(article_id)
            doc = doc_ref.get()

            if not doc.exists:
                raise ValueError(f"Artículo con ID {article_id} no encontrado")

            current_data = doc.to_dict()
            new_version = current_data["version"] + 1

            # Actualizar datos
            update_data["updated_at"] = datetime.utcnow()
            update_data["version"] = new_version

            # Guardar en Firestore
            doc_ref.update(update_data)

            # Crear nueva versión
            new_data = {**current_data, **update_data}
            FirestoreManager.create_article_version(article_id, new_data, new_version)

            print(f"✅ Artículo actualizado: {article_id} (versión {new_version})")
            return new_version

        except Exception as e:
            print(f"❌ Error al actualizar artículo: {str(e)}")
            raise e
    
    @staticmethod
    def delete_article(article_id: str) -> bool:
        """
            Eliminar un artículo (soft delete)

            Args:
                article_id: ID del artículo
            
            Returns:
                bool: True si se eliminó correctamente
        """
        try:
            # Soft delete: actualizar status a "archived"
            db_client = get_db()
            if db_client is None:
                raise Exception("Firestore no disponible")
            db_client.collection("articles").document(article_id).update({
                "status": "archived",
                "updated_at": datetime.utcnow()
            })

            print(f"✅ Artículo archivado: {article_id}")
            return True

        except Exception as e:
            print(f"❌ Error al eliminar (archivar) artículo: {str(e)}")
            raise e
        
    @staticmethod
    def create_article_version(article_id: str, article_data: Dict, version: int):
        """
            Crear versión del artículo en colección separada

            Args:
                article_id: ID del artículo
                article_data: Datos del artículo
                version: Número de versión
        """
        try:
            version_data = {
                "article_id": article_id,
                "version": version,
                "data": article_data,
                "created_at": datetime.utcnow()
            }

            db_client = get_db()
            if db_client is None:
                print("⚠️  Firestore no disponible, saltando creación de versión")
                return
            db_client.collection("article_versions").add(version_data)
            print(f"✅ Versión {version} creada para artículo {article_id}")

        except Exception as e:
            print(f"❌ Error al crear versión del artículo: {str(e)}")
            # No re-lanzar la excepción para no interrumpir la creación del artículo
            pass
        
    @staticmethod
    def get_article_versions(article_id: str) -> List[Dict]:
        """
            Obtener historial de versiones de un artículo

            Args: 
                article_id: ID del artículo
            
            Returns:
                List[Dict]: Lista de versiones
        """
        try:
            db_client = get_db()
            if db_client is None:
                raise Exception("Firestore no disponible")
            versions = db_client.collection("article_versions")\
                .where("article_id", "==", article_id)\
                .order_by("version", direction=firestore.Query.DESCENDING)\
                .stream()

            version_list = []
            for doc in versions:
                version_list.append({"id": doc.id, **doc.to_dict()})

            print(f"✅ {len(version_list)} versiones encontradas para artículo {article_id}")
            return version_list

        except Exception as e:
            print(f"❌ Error al obtener versiones del artículo: {str(e)}")
            raise e
            
