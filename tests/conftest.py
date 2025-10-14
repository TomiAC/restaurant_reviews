# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
import os
from unittest.mock import MagicMock
from dotenv import load_dotenv
from pymongo.uri_parser import parse_uri

# Cargar variables de entorno
load_dotenv()

# Importar la app despues de configurar mocks/variables si es necesario
from app.main import app

# Usar una base de datos de prueba real
TEST_MONGO_URI = os.getenv("MONGODB_URI_TEST")
if not TEST_MONGO_URI:
    raise ValueError("La variable de entorno MONGODB_URI_TEST no está configurada. Por favor, configúrala en tu archivo .env.")

# Extraer el nombre de la DB de la URI o usar uno por defecto
parsed_uri = parse_uri(TEST_MONGO_URI)
TEST_DB_NAME = parsed_uri.get('database', 'test_restaurant_reviews_db')


@pytest.fixture(scope="session")
def test_mongo_client():
    client = MongoClient(TEST_MONGO_URI)
    yield client
    client.close()

@pytest.fixture(scope="session")
def test_db(test_mongo_client):
    db = test_mongo_client[TEST_DB_NAME]
    yield db
    # Limpiar la base de datos de prueba después de la sesión
    test_mongo_client.drop_database(TEST_DB_NAME)

@pytest.fixture(autouse=True)
def auto_clean_db(test_db):
    """Limpia las colecciones antes de cada prueba para asegurar aislamiento."""
    test_db.restaurants.delete_many({})
    test_db.reviews.delete_many({})
    test_db.users.delete_many({})
    yield

@pytest.fixture
def client(monkeypatch, test_db):
    """
    Prepara el cliente de prueba de FastAPI, mockeando las dependencias
    de base de datos y Redis.
    """
    # Mockear las colecciones en el módulo de base de datos
    monkeypatch.setattr("app.database.restaurants_collection", test_db.restaurants)
    monkeypatch.setattr("app.database.reviews_collection", test_db.reviews)
    monkeypatch.setattr("app.database.user_collection", test_db.users)
    
    # Mockear el cliente de Redis
    mock_redis = MagicMock()
    mock_redis.get.return_value = None  # Por defecto, no hay nada en caché
    monkeypatch.setattr("app.database.redis_client", mock_redis)
    monkeypatch.setattr("app.routers.reviews.redis_client", mock_redis)

    with TestClient(app) as c:
        yield c

@pytest.fixture
def test_restaurant(test_db):
    """Inserta un restaurante de prueba y devuelve su ID."""
    result = test_db.restaurants.insert_one({"name": "Testaurant", "description": "Un restaurante de prueba"})
    return str(result.inserted_id)
