import pytest
from tests.conftest import client, auth_headers, sample_product

def test_create_product(client, auth_headers, sample_product):
    """Test creating a product."""
    response = client.post("/products", json=sample_product, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_product["name"]
    assert data["price"] == sample_product["price"]
    assert "id" in data

def test_create_product_unauthenticated(client, sample_product):
    """Test creating a product without authentication."""
    response = client.post("/products", json=sample_product)
    assert response.status_code == 401

def test_list_products(client, auth_headers, sample_product):
    """Test listing products."""
    client.post("/products", json=sample_product, headers=auth_headers)
    
    response = client.get("/products", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == sample_product["name"]

def test_get_product(client, auth_headers, sample_product):
    """Test getting a single product."""
    create_response = client.post("/products", json=sample_product, headers=auth_headers)
    product_id = create_response.json()["id"]
    
    response = client.get(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == sample_product["name"]

def test_get_product_not_found(client, auth_headers):
    """Test getting a non-existent product."""
    response = client.get("/products/99999", headers=auth_headers)
    assert response.status_code == 404

def test_update_product(client, auth_headers, sample_product):
    """Test updating a product."""
    create_response = client.post("/products", json=sample_product, headers=auth_headers)
    product_id = create_response.json()["id"]
    
    update_data = {
        "name": "Updated Product",
        "price": 149.99
    }
    response = client.patch(
        f"/products/{product_id}",
        json=update_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]
    assert response.json()["price"] == update_data["price"]

def test_delete_product(client, auth_headers, sample_product):
    """Test deleting a product."""
    create_response = client.post("/products", json=sample_product, headers=auth_headers)
    product_id = create_response.json()["id"]
    
    response = client.delete(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 204
    
    response = client.get(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 404
