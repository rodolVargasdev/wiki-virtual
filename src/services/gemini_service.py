# import google.generativeai as genai  # DESACTIVADO
import os
from typing import List, Dict

class GeminiService:
    """Servicio para interactuar con Gemini API (MODO DEGRADADO)"""
    
    def __init__(self):
        """Inicializar servicio de Gemini en modo degradado"""
        print("⚠️  GeminiService en MODO DEGRADADO - IA desactivada")
        
        # API desactivada para arranque rápido
        self.model = None
        
        print("✅ GeminiService inicializado en modo degradado")
    
    def generate_answer(self, query: str, context: str) -> str:
        """
        Generar respuesta usando Gemini (MODO DEGRADADO)
        
        Args:
            query: Pregunta del usuario
            context: Contexto de artículos
            
        Returns:
            str: Respuesta generada (modo degradado)
        """
        print("⚠️  Modo degradado: Generando respuesta simple")
        
        # Respuesta simple basada en contexto
        if context and len(context) > 100:
            # Extraer información relevante del contexto
            context_preview = context[:500] + "..." if len(context) > 500 else context
            
            return f"""Respuesta basada en la información disponible:

{context_preview}

Nota: Esta respuesta se generó en modo degradado. Para respuestas más precisas, 
activa el servicio de Gemini en la configuración."""
        else:
            return f"""No se encontró información suficiente para responder a: "{query}"

Por favor, verifica que los artículos relevantes estén cargados en el sistema.
Modo degradado activo - respuestas limitadas."""
    
    def test_connection(self) -> bool:
        """
        Probar conexión con Gemini (MODO DEGRADADO)
        
        Returns:
            bool: False (siempre en modo degradado)
        """
        print("⚠️  Modo degradado: Gemini desactivado")
        return False

# Instancia global del servicio de Gemini
gemini_service = GeminiService()