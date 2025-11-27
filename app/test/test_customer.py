from fastapi import status


def test_create_customer(client):
    response = client.post(
        "/api/customers",
        json={
            "name": "Marco",
            "email": "marco@example.com",
            "age": 43
        }
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_read_customer(client):
    response = client.post(
        "/api/customers",
        json={
            "name": "Diego",
            "email": "diego@example.com",
            "age": 43
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    customer_id: int = response.json()["id"]
    response_read = client.get(
        f"/api/customers/{customer_id}"
    )
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json()["name"] == "Diego"
