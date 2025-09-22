#!/bin/bash

# Script de despliegue para Google Cloud Run
# Uso: ./deploy.sh [PROJECT_ID] [REGION]

set -e

# Configuración
PROJECT_ID=${1:-"wiki-virtual-python-20f8f"}
REGION=${2:-"us-central1"}
SERVICE_NAME="wiki-virtual-api"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Desplegando Wiki Virtual a Google Cloud Run..."
echo "📋 Proyecto: $PROJECT_ID"
echo "🌍 Región: $REGION"
echo "🐳 Imagen: $IMAGE_NAME"

# 1. Configurar proyecto
echo "⚙️  Configurando proyecto..."
gcloud config set project $PROJECT_ID

# 2. Habilitar APIs necesarias
echo "🔧 Habilitando APIs..."
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com

# 3. Construir imagen Docker
echo "🐳 Construyendo imagen Docker..."
gcloud builds submit --tag $IMAGE_NAME

# 4. Desplegar a Cloud Run
echo "🚀 Desplegando a Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10 \
  --set-env-vars="ENVIRONMENT=production" \
  --set-env-vars="PORT=8080"

# 5. Obtener URL del servicio
echo "✅ Despliegue completado!"
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')
echo "🌐 URL del servicio: $SERVICE_URL"
echo "📚 Documentación: $SERVICE_URL/docs"
echo "❤️  Health check: $SERVICE_URL/health"


