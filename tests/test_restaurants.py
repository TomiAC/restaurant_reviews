from fastapi.testclient import TestClient
from bson import ObjectId

def test_get_reviews_for_restaurant_success(client: TestClient, test_restaurant: str, test_db):
    """
    Prueba que se pueden obtener las reviews de un restaurante existente.
    """
    # Añadir algunas reviews de prueba
    review_1 = {
        "restaurant_id": ObjectId(test_restaurant),
        "text": "Review 1",
        "rating": 4,
        "author_name": "Author 1"
    }
    review_2 = {
        "restaurant_id": ObjectId(test_restaurant),
        "text": "Review 2",
        "rating": 5,
        "author_name": "Author 2"
    }
    test_db.reviews.insert_many([review_1, review_2])

    response = client.get(f"/restaurants/{test_restaurant}/reviews")

    assert response.status_code == 200
    data = response.json()
    assert "reviews" in data
    assert len(data["reviews"]) == 2
    assert data["reviews"][0]["text"] == "Review 1"

def test_get_reviews_for_restaurant_no_reviews(client: TestClient, test_restaurant: str):
    """
    Prueba la respuesta cuando un restaurante no tiene reviews.
    """
    response = client.get(f"/restaurants/{test_restaurant}/reviews")

    assert response.status_code == 200
    assert response.json() == {"message": "No reviews found for this restaurant"}

def test_get_reviews_for_restaurant_invalid_id(client: TestClient):
    """
    Prueba que la API devuelve 400 si el ID del restaurante es inválido.
    """
    response = client.get("/restaurants/invalid-id/reviews")

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid restaurant ID"}

def test_search_restaurants_by_name_success(client: TestClient, test_restaurant):
    """
    Prueba la búsqueda exitosa de un restaurante por nombre.
    """
    response = client.get("/restaurants/search?name=Testaurant")

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Testaurant"
    assert data[0]["_id"] == test_restaurant

def test_search_restaurants_by_name_no_results(client: TestClient):
    """
    Prueba la búsqueda de un restaurante que no existe.
    """
    response = client.get("/restaurants/search?name=NonExistent")

    assert response.status_code == 200
    assert response.json() == []
