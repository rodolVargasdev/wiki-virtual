import requests
import json
from test_auth import get_id_token

def test_rag_advanced():
    """Test avanzado del sistema RAG con múltiples artículos"""
    
    # Obtener token de autenticación
    token = get_id_token("admin@example.com", "qw12QW")
    if not token:
        print("❌ No se pudo obtener token")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    base_url = "http://localhost:8000"
    
    # 1. Crear múltiples artículos de diferentes temas
    print("📚 Creando múltiples artículos...")
    
    articles = [
        {
            "title": "Introducción a Redes de Computadoras",
            "content": "Las redes de computadoras son sistemas que permiten la comunicación entre dispositivos. Existen diferentes tipos de redes como LAN (Local Area Network), WAN (Wide Area Network) y MAN (Metropolitan Area Network). Las redes utilizan protocolos como TCP/IP para la comunicación. La topología de red define cómo están conectados los dispositivos, siendo las más comunes la estrella, bus y anillo.",
            "category": "Tecnología",
            "tags": ["redes", "computación", "protocolos", "topología"],
            "visibility": "public"
        },
        {
            "title": "Fundamentos de Programación en Python",
            "content": "Python es un lenguaje de programación de alto nivel, interpretado y de propósito general. Fue creado por Guido van Rossum en 1991. Python se caracteriza por su sintaxis clara y legible, lo que lo hace ideal para principiantes. Los conceptos básicos incluyen variables, tipos de datos, estructuras de control (if, for, while), funciones y clases. Python es ampliamente usado en desarrollo web, ciencia de datos, inteligencia artificial y automatización.",
            "category": "Programación",
            "tags": ["python", "programación", "lenguaje", "sintaxis"],
            "visibility": "public"
        },
        {
            "title": "Bases de Datos Relacionales",
            "content": "Una base de datos relacional es un tipo de base de datos que almacena información en tablas relacionadas entre sí. Cada tabla tiene filas (registros) y columnas (campos). Las relaciones se establecen mediante claves primarias y claves foráneas. SQL (Structured Query Language) es el lenguaje estándar para consultar y manipular bases de datos relacionales. Los sistemas de gestión de bases de datos más populares incluyen MySQL, PostgreSQL, Oracle y SQL Server.",
            "category": "Bases de Datos",
            "tags": ["bases de datos", "SQL", "relacional", "tablas"],
            "visibility": "public"
        },
        {
            "title": "Inteligencia Artificial y Machine Learning",
            "content": "La inteligencia artificial (IA) es una rama de la informática que se enfoca en crear sistemas capaces de realizar tareas que normalmente requieren inteligencia humana. El machine learning es un subcampo de la IA que permite a las máquinas aprender de los datos sin ser programadas explícitamente. Los algoritmos de machine learning incluyen regresión lineal, árboles de decisión, redes neuronales y clustering. Las aplicaciones de IA incluyen reconocimiento de voz, procesamiento de lenguaje natural, visión por computadora y sistemas de recomendación.",
            "category": "Inteligencia Artificial",
            "tags": ["IA", "machine learning", "algoritmos", "redes neuronales"],
            "visibility": "public"
        },
        {
            "title": "Desarrollo Web con HTML, CSS y JavaScript",
            "content": "El desarrollo web frontend se basa en tres tecnologías principales: HTML (HyperText Markup Language) para la estructura, CSS (Cascading Style Sheets) para el diseño y JavaScript para la interactividad. HTML define la estructura y contenido de las páginas web usando elementos como div, p, h1, img y form. CSS controla la presentación visual incluyendo colores, fuentes, espaciado y layout. JavaScript permite crear páginas dinámicas e interactivas, manejar eventos del usuario y comunicarse con servidores.",
            "category": "Desarrollo Web",
            "tags": ["HTML", "CSS", "JavaScript", "frontend", "web"],
            "visibility": "public"
        }
    ]
    
    created_articles = []
    
    for i, article_data in enumerate(articles, 1):
        print(f"📝 Creando artículo {i}/5: {article_data['title']}")
        
        response = requests.post(f"{base_url}/articles/", json=article_data, headers=headers)
        if response.status_code == 200:
            article_id = response.json()["article_id"]
            created_articles.append({
                "id": article_id,
                "title": article_data["title"],
                "category": article_data["category"]
            })
            print(f"✅ Artículo creado: {article_id}")
        else:
            print(f"❌ Error creando artículo {i}: {response.text}")
            return
    
    print(f"\n🎉 {len(created_articles)} artículos creados exitosamente!")
    
    # 2. Hacer preguntas específicas y detalladas
    print("\n🤖 Haciendo preguntas específicas al sistema RAG...")
    
    questions = [
        {
            "question": "¿Cuáles son los diferentes tipos de redes de computadoras y cómo se clasifican?",
            "expected_topic": "redes",
            "expected_article": "Introducción a Redes de Computadoras"
        },
        {
            "question": "¿Qué es Python y cuáles son sus características principales como lenguaje de programación?",
            "expected_topic": "python",
            "expected_article": "Fundamentos de Programación en Python"
        },
        {
            "question": "¿Cómo funcionan las bases de datos relacionales y qué es SQL?",
            "expected_topic": "bases de datos",
            "expected_article": "Bases de Datos Relacionales"
        }
    ]
    
    for i, q in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"❓ PREGUNTA {i}: {q['question']}")
        print(f"🎯 Tema esperado: {q['expected_topic']}")
        print(f"�� Artículo esperado: {q['expected_article']}")
        print(f"{'='*60}")
        
        chat_data = {
            "message": q["question"],
            "max_results": 3
        }
        
        response = requests.post(f"{base_url}/chat/", json=chat_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ RESPUESTA:")
            print(f"   {result['answer']}")
            print(f"\n�� CONFIANZA: {result['confidence']:.3f}")
            print(f"📚 FUENTES ENCONTRADAS: {len(result['sources'])}")
            
            # Mostrar detalles de cada fuente
            for j, source in enumerate(result['sources'], 1):
                print(f"\n   📖 FUENTE {j}:")
                print(f"      Título: {source['title']}")
                print(f"      ID: {source['id']}")
                print(f"      Similitud: {source['similarity_score']:.3f}")
                print(f"      Preview: {source['content_preview']}")
                
                # Verificar si es el artículo esperado
                if q['expected_article'] in source['title']:
                    print(f"      ✅ ¡ARTÍCULO CORRECTO ENCONTRADO!")
                else:
                    print(f"      ⚠️ Artículo diferente al esperado")
            
            # Análisis de la respuesta
            print(f"\n🔍 ANÁLISIS:")
            if result['confidence'] > 0.7:
                print(f"   ✅ Alta confianza en la respuesta")
            elif result['confidence'] > 0.4:
                print(f"   ⚠️ Confianza moderada en la respuesta")
            else:
                print(f"   ❌ Baja confianza en la respuesta")
                
            if len(result['sources']) > 0:
                print(f"   ✅ Se encontraron fuentes relevantes")
            else:
                print(f"   ❌ No se encontraron fuentes")
                
        else:
            print(f"❌ Error en chat: {response.text}")
    
    # 3. Obtener estadísticas finales
    print(f"\n{'='*60}")
    print("📊 ESTADÍSTICAS FINALES DEL SISTEMA")
    print(f"{'='*60}")
    
    response = requests.get(f"{base_url}/chat/stats", headers=headers)
    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Estadísticas del sistema:")
        print(f"   - Total de artículos indexados: {stats['embedding_stats']['total_articles']}")
        print(f"   - Embeddings cargados: {stats['embedding_stats']['embeddings_loaded']}")
        print(f"   - Modelo usado: {stats['embedding_stats']['model_name']}")
    else:
        print(f"❌ Error obteniendo estadísticas: {response.text}")
    
    # 4. Resumen de artículos creados
    print(f"\n📚 RESUMEN DE ARTÍCULOS CREADOS:")
    for article in created_articles:
        print(f"   - {article['title']} (Categoría: {article['category']})")
    
    print(f"\n�� Test avanzado completado exitosamente!")

if __name__ == "__main__":
    test_rag_advanced()