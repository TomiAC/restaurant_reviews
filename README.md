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

---

# 🍽️ Restaurant Review API with NLP & Leaderboard (English)

This is a backend project built with **FastAPI**, which allows users to add restaurant reviews. It uses **Natural Language Processing (NLP)** to automatically classify reviews as positive or negative and maintains a **live ranking** of restaurants based on these reviews.

---

## 🚀 Technologies Used

- 🐍 Python 3.10+
- ⚡ [FastAPI](https://fastapi.tiangolo.com/) – Modern and fast web framework
- 🍃 [MongoDB](https://www.mongodb.com/) – NoSQL database
- 📚 [Pymongo](https://pymongo.readthedocs.io/en/stable/) – MongoDB client for Python
- 💬 [TextBlob](https://textblob.readthedocs.io/en/dev/) – NLP library for sentiment analysis
- 🖼️ Jinja2 – For rendering HTML from the backend
- 🧪 HTML, JavaScript, CSS – Simple interface to display the ranking and add reviews

## 📊 Main Features
📥 Add Reviews: Users can search for a restaurant and submit a review from the browser.

🤖 Sentiment Analysis: Each review is automatically classified as positive or negative using TextBlob.

🏆 Leaderboard: A ranking of restaurants is displayed based on the number of positive reviews minus the negative ones.

🔍 Restaurant Search: To facilitate adding reviews to specific restaurants.

🗃️ Initial Load: Data can be imported from a CSV file to preload restaurants and reviews.

##🧪 Main Endpoints
| Method | Path                           | Description                              |
| ------ | ------------------------------ | ---------------------------------------- |
| GET    | `/`                            | HTML page with ranking and form          |
| POST   | `/review`                      | Add a new review with NLP analysis       |
| GET    | `/leaderboard`                 | Get restaurant ranking                   |
| GET    | `/restaurants/search?name=...` | Search for a restaurant by name          |
| GET    | `/restaurants/{id}/reviews`    | View reviews for a specific restaurant   |

## Restaurant Reviews Dataset
The data loaded was obtained from the following dataset: https://www.kaggle.com/datasets/denizbilginn/google-maps-restaurant-reviews .

## Contact
www.linkedin.com/in/ta-cardozo