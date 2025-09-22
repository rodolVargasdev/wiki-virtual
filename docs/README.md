# 🐍 Wiki Virtual Backend - FastAPI + Firebase + RAG

## 📋 Descripción del Proyecto

**Wiki Virtual** es una biblioteca educativa inteligente que combina FastAPI, Firebase y técnicas de RAG (Retrieval-Augmented Generation) para crear un sistema de gestión de conocimiento con chat con IA.

### 🎯 Características Principales

- ✅ **API REST moderna** con FastAPI
- ✅ **Autenticación segura** con Firebase Auth
- ✅ **Base de datos NoSQL** con Firestore
- ✅ **Chat con IA** usando Gemini API
- ✅ **Búsqueda semántica** con embeddings locales
- ✅ **Control de versiones** de artículos
- ✅ **Sistema de roles** (admin, usuario)
- ✅ **Despliegue en Google Cloud Run**

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Firebase      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (Auth + DB)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Gemini API    │
                       │   (IA Chat)     │
                       └─────────────────┘
```

---

## 🚀 Tecnologías Utilizadas

### Backend Core
- **FastAPI 0.104.1** - Framework web moderno y rápido
- **Python 3.11** - Lenguaje de programación
- **Uvicorn** - Servidor ASGI de alto rendimiento

### Base de Datos y Autenticación
- **Firebase Firestore** - Base de datos NoSQL
- **Firebase Authentication** - Sistema de autenticación
- **Firebase Admin SDK** - SDK para operaciones del servidor

### Inteligencia Artificial
- **Google Gemini API** - Modelo de IA para chat
- **sentence-transformers** - Embeddings locales (gratuitos)
- **NumPy** - Cálculos numéricos para similitud

### Despliegue y DevOps
- **Google Cloud Run** - Plataforma serverless
- **Docker** - Containerización
- **Firebase Hosting** - Hosting del frontend

---

## 📁 Estructura del Proyecto

```
wiki-virtual/
├── 📄 main.py                 # Aplicación principal FastAPI
├── 🔐 auth.py                 # Autenticación y autorización
├── 📝 articles.py             # CRUD de artículos
├── 🤖 chat.py                 # Endpoint de chat con IA
├── 🔥 firebase_config.py      # Configuración de Firebase
├── 🧠 embeddings.py           # Gestión de embeddings
├── 🗄️ firestore_utils.py     # Utilidades de Firestore
├── 📊 models.py               # Modelos Pydantic
├── 🧪 test_*.py               # Scripts de prueba
├── 🐳 Dockerfile              # Configuración de Docker
├── 📦 requirements.txt        # Dependencias Python
├── 🔑 firebase-key.json       # Credenciales Firebase
├── ⚙️ .env                    # Variables de entorno
└── 📖 README.md               # Este archivo
```

---

## 🛠️ Instalación y Configuración

### Prerrequisitos

- **Python 3.11+**
- **Google Cloud CLI**
- **Firebase CLI**
- **Docker** (opcional)

### 1. Clonar el Repositorio

```bash
git clone <tu-repositorio>
cd wiki-virtual
```

### 2. Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Firebase

1. **Crear proyecto en [Firebase Console](https://console.firebase.google.com)**
2. **Activar servicios**:
   - Firebase Authentication
   - Firestore Database
   - Firebase Storage
3. **Generar clave de servicio** y descargar `firebase-key.json`
4. **Configurar autenticación** con Google

### 5. Configurar Variables de Entorno

Crear archivo `.env`:

```env
# Firebase Configuration
FIREBASE_PROJECT_ID=tu-proyecto-firebase
FIREBASE_API_KEY=tu-api-key-firebase
ALLOWED_DOMAINS=example.com,tu-empresa.com
ALLOWED_EMAILS=admin@example.com,test@example.com

# Gemini API
GEMINI_API_KEY=tu-api-key-gemini

# Environment
ENVIRONMENT=development
```

### 6. Ejecutar en Desarrollo

```bash
uvicorn main:app --reload
```

La API estará disponible en: `http://localhost:8000`

---

## 📚 Documentación de la API

### Endpoints Principales

#### 🔍 Información General
- `GET /` - Información de la API
- `GET /health` - Estado de salud del servicio
- `GET /docs` - Documentación interactiva (Swagger)

#### 🔐 Autenticación
- `GET /profile` - Perfil del usuario autenticado
- `GET /admin-only` - Endpoint solo para administradores

#### 📝 Artículos
- `GET /articles` - Listar artículos
- `POST /articles` - Crear artículo (admin)
- `GET /articles/{id}` - Obtener artículo específico
- `PUT /articles/{id}` - Actualizar artículo (admin)
- `GET /articles/{id}/versions` - Historial de versiones

#### 🤖 Chat con IA
- `POST /chat` - Enviar mensaje al chat
- `POST /chat/reindex` - Reindexar artículos (admin)

### Autenticación

Todos los endpoints (excepto `/` y `/health`) requieren autenticación:

```bash
# Header requerido
Authorization: Bearer <firebase-id-token>
```

### Ejemplo de Uso

```bash
# Obtener token de Firebase
curl -X POST "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password","returnSecureToken":true}'

# Usar token en la API
curl -X GET "http://localhost:8000/articles" \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN"
```

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Test completo del sistema
python test_complete_system.py

# Test de autenticación
python test_auth.py

# Test de embeddings
python test_embeddings_free.py

# Test de Gemini
python test_gemini.py
```

### Verificar Configuración

```bash
# Verificar variables de entorno
python check_env.py

# Verificar Firebase Admin
python check_firebase_admin.py
```

---

## 🚀 Despliegue en Producción

### Google Cloud Run

```bash
# Configurar proyecto
gcloud config set project tu-proyecto-gcp

# Habilitar APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# Desplegar
gcloud run deploy wiki-virtual-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="FIREBASE_PROJECT_ID=tu-proyecto,GEMINI_API_KEY=tu-key,ENVIRONMENT=production"
```

### Variables de Entorno en Producción

```bash
FIREBASE_PROJECT_ID=tu-proyecto-firebase
GEMINI_API_KEY=tu-api-key-gemini
ALLOWED_DOMAINS=example.com,tu-empresa.com
ALLOWED_EMAILS=admin@example.com,test@example.com
ENVIRONMENT=production
```

---

## 🔧 Configuración Avanzada

### Sistema de Roles

```python
# Roles disponibles
- admin: Acceso completo
- user: Acceso de lectura
- editor: Puede crear/editar artículos
```

### Embeddings y RAG

```python
# Configuración de embeddings
- Modelo: all-MiniLM-L6-v2 (sentence-transformers)
- Almacenamiento: In-memory (numpy arrays)
- Búsqueda: Cosine similarity
- Threshold: 0.7 para relevancia
```

### Límites y Cuotas

```python
# Límites por defecto
- Artículos por página: 10
- Resultados de búsqueda: 3
- Tamaño máximo de artículo: 1MB
- Rate limiting: 100 req/min por usuario
```

---

## 🐛 Troubleshooting

### Problemas Comunes

#### 1. Error de Autenticación
```bash
# Verificar token
python regenerate_token.py

# Verificar configuración
python check_firebase_admin.py
```

#### 2. Error de Embeddings
```bash
# Reinstalar dependencias
pip install --upgrade sentence-transformers numpy
```

#### 3. Error de Gemini
```bash
# Verificar API key
python test_gemini.py

# Verificar modelos disponibles
python test_gemini_models.py
```

#### 4. Error de Firestore
```bash
# Verificar índices
# Ir a Firebase Console > Firestore > Indexes
# Crear índice compuesto si es necesario
```

### Logs y Debugging

```bash
# Ver logs en desarrollo
uvicorn main:app --reload --log-level debug

# Ver logs en producción
gcloud logging read "resource.type=cloud_run_revision" --limit 50
```

---

## 📊 Monitoreo y Métricas

### Health Checks

```bash
# Endpoint de salud
curl https://tu-api.run.app/health

# Respuesta esperada
{
  "status": "healthy",
  "message": "API funcionando correctamente",
  "port": 8080,
  "environment": "production"
}
```

### Métricas Importantes

- **Tiempo de respuesta** de la API
- **Uso de memoria** y CPU
- **Número de requests** por minuto
- **Errores** de autenticación
- **Uso de Gemini API**

---

## 🤝 Contribución

### Cómo Contribuir

1. **Fork** el repositorio
2. **Crear branch** para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. **Push** al branch (`git push origin feature/nueva-funcionalidad`)
5. **Crear Pull Request**

### Estándares de Código

- **PEP 8** para Python
- **Type hints** en todas las funciones
- **Docstrings** para documentación
- **Tests** para nuevas funcionalidades

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👥 Autores

- **JOSE-** - Desarrollador Principal
- **Asistente IA** - Mentor y Guía Pedagógica

---

## 🔗 Enlaces Útiles

- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [Firebase Python SDK](https://firebase.google.com/docs/admin/setup)
- [Google Cloud Run](https://cloud.google.com/run/docs)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [sentence-transformers](https://www.sbert.net/)

---

## 📞 Soporte

Si tienes problemas o preguntas:

1. **Revisar** la documentación
2. **Ejecutar** los scripts de test
3. **Verificar** la configuración
4. **Crear issue** en el repositorio

---

*Última actualización: $(date)*  
*Versión: 1.0.0*  
*Estado: En Producción* 🚀
