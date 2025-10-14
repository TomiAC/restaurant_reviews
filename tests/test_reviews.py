from fastapi.testclient import TestClient
from unittest.mock import MagicMock

def test_add_review_success(client: TestClient, test_restaurant: str, monkeypatch):
    """
    Prueba la creación exitosa de una review.
    """
    # Mockear analyze_sentiment para que devuelva un valor predecible
    mock_analyze = MagicMock(return_value="positive")
    monkeypatch.setattr("app.routers.reviews.analyze_sentiment", mock_analyze)

    review_data = {
        "restaurant_id": test_restaurant,
        "text": "¡Este lugar es genial!",
        "rating": 5,
        "author_name": "Testy McTesterson"
    }
    response = client.post("/reviews/", json=review_data)
    
    assert response.status_code == 200
    assert response.json() == {"sentiment": "positive"}
    
    # Verificar que analyze_sentiment fue llamado
    mock_analyze.assert_called_once_with("¡Este lugar es genial!")

    # Verificar que la caché de Redis fue limpiada
    from app.routers.reviews import redis_client
    redis_client.delete.assert_called_once_with("leaderboard")


def test_add_review_restaurant_not_found(client: TestClient):
    """
    Prueba que la API devuelve 404 si el restaurante no existe.
    """
    # Un ObjectId que probablemente no existe
    non_existent_id = "60c72b9f9b1d8b001f8e4b8b"
    review_data = {
        "restaurant_id": non_existent_id,
        "text": "Este lugar no existe.",
        "rating": 1,
        "author_name": "Ghost Writer"
    }
    response = client.post("/reviews/", json=review_data)
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Restaurante no encontrado"}


def test_add_review_invalid_data(client: TestClient, test_restaurant: str):
    """
    Prueba que la API devuelve 422 si faltan datos en la petición.
    """
    # Petición sin el campo 'text'
    review_data = {
        "restaurant_id": test_restaurant,
        "rating": 5,
        "author_name": "Incomplete Tester"
    }
    response = client.post("/reviews/", json=review_data)
    
    assert response.status_code == 422  # Unprocessable Entity
