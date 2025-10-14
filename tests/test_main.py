from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import json

def test_root(client: TestClient):
    """
    Prueba que el endpoint principal devuelve HTML.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers['content-type']

def test_get_leaderboard_empty(client: TestClient):
    """
    Prueba que el leaderboard está vacío cuando no hay reviews.
    """
    response = client.get("/leaderboard")
    assert response.status_code == 200
    assert response.json() == {"leaderboard": []}

def test_get_leaderboard_with_data(client: TestClient, monkeypatch):
    """
    Prueba que el leaderboard devuelve datos cacheados de Redis.
    """
    # Mockear el cliente de Redis para que devuelva un leaderboard de prueba
    mock_leaderboard_data = [{"name": "Restaurant A", "score": 10}]
    mock_redis = MagicMock()
    mock_redis.get.return_value = json.dumps(mock_leaderboard_data)
    monkeypatch.setattr("app.database.redis_client", mock_redis)

    response = client.get("/leaderboard")
    assert response.status_code == 200
    assert response.json() == {"leaderboard": mock_leaderboard_data}
    # Verificar que se llamó a redis.get
    mock_redis.get.assert_called_once_with("leaderboard")

def test_get_leaderboard_pagination(client: TestClient, monkeypatch):
    """
    Prueba la paginación del leaderboard.
    """
    # Crear un leaderboard grande para mockear
    mock_leaderboard_data = [{"name": f"Restaurant {i}", "score": 20 - i} for i in range(15)]
    mock_redis = MagicMock()
    mock_redis.get.return_value = json.dumps(mock_leaderboard_data)
    monkeypatch.setattr("app.database.redis_client", mock_redis)

    # Pedir la primera página (debería tener 10 elementos)
    response_page_0 = client.get("/leaderboard?page=0")
    assert response_page_0.status_code == 200
    assert len(response_page_0.json()["leaderboard"]) == 10

    # Pedir la segunda página (debería tener 5 elementos)
    response_page_1 = client.get("/leaderboard?page=1")
    assert response_page_1.status_code == 200
    assert len(response_page_1.json()["leaderboard"]) == 5
    assert response_page_1.json()["leaderboard"][0]["name"] == "Restaurant 10"
