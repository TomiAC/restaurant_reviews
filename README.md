# 🍽️ Restaurant Review API with NLP & Leaderboard

Este es un proyecto backend construido con **FastAPI**, que permite a los usuarios agregar reseñas de restaurantes. Utiliza **procesamiento de lenguaje natural (NLP)** para clasificar automáticamente las reseñas como positivas o negativas y mantiene un **ranking en vivo** de los restaurantes basado en estas reseñas.

---

## 🚀 Tecnologías utilizadas

- 🐍 Python 3.10+
- ⚡ [FastAPI](https://fastapi.tiangolo.com/) – Framework web moderno y rápido
- 🍃 [MongoDB](https://www.mongodb.com/) – Base de datos NoSQL
- 📚 [Pymongo](https://pymongo.readthedocs.io/en/stable/) – Cliente MongoDB para Python
- 💬 [TextBlob](https://textblob.readthedocs.io/en/dev/) – Biblioteca de NLP para análisis de sentimiento
- 🖼️ Jinja2 – Para renderizar HTML desde el backend
- 🧪 HTML, JavaScript, CSS – Interfaz simple para mostrar el ranking y agregar reseñas

## 📊 Funcionalidades principales
📥 Agregar reseñas: Los usuarios pueden buscar un restaurante y enviar una reseña desde el navegador.

🤖 Análisis de Sentimiento: Cada reseña se clasifica automáticamente como positiva o negativa usando TextBlob.

🏆 Leaderboard: Se muestra un ranking de restaurantes basado en la cantidad de reseñas positivas menos las negativas.

🔍 Búsqueda de restaurantes: Para facilitar la carga de reseñas a restaurantes específicos.

🗃️ Carga inicial: Se pueden importar datos desde CSV para precargar restaurantes y reseñas.

##🧪 Endpoints principales
| Método | Ruta                           | Descripción                              |
| ------ | ------------------------------ | ---------------------------------------- |
| GET    | `/`                            | Página HTML con ranking y formulario     |
| POST   | `/review`                      | Agregar nueva reseña con análisis NLP    |
| GET    | `/leaderboard`                 | Obtener ranking de restaurantes          |
| GET    | `/restaurants/search?name=...` | Buscar restaurante por nombre            |
| GET    | `/restaurants/{id}/reviews`    | Ver reseñas de un restaurante específico |

## Restaurant Reviews Dataset
Los datos cargados fueron obtenidos del siguiente dataset: https://www.kaggle.com/datasets/denizbilginn/google-maps-restaurant-reviews .

## Contacto
www.linkedin.com/in/ta-cardozo
