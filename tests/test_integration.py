import pytest
from tests.conftest import client

def test_full_crud_flow(client):
    """Test the full CRUD flow from registration to deletion."""
    
    # 1. Register a user
    user_data = {
        "username": "integration_user",
        "email": "integration@example.com",
        "password": "testpass123",
        "full_name": "Integration User"
    }
    register_response = client.post("/register", json=user_data)
    assert register_response.status_code == 201
    
    # 2. Login
    login_response = client.post(
        "/login",
        data={
            "username": user_data["username"],
            "password": user_data["password"]
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Create a product
    product_data = {
        "name": "Integration Test Product",
        "description": "Created during integration test",
        "price": 79.99,
        "stock": 20
    }
    create_response = client.post("/products", json=product_data, headers=headers)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]
    assert product_data["name"] == create_response.json()["name"]
    
    # 4. Get the product
    get_response = client.get(f"/products/{product_id}", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["name"] == product_data["name"]
    
    # 5. Update the product
    update_data = {
        "name": "Updated Integration Product",
        "price": 89.99,
        "stock": 15
    }
    update_response = client.patch(
        f"/products/{product_id}",
        json=update_data,
        headers=headers
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == update_data["name"]
    assert update_response.json()["price"] == update_data["price"]
    
    # 6. Delete the product
    delete_response = client.delete(f"/products/{product_id}", headers=headers)
    assert delete_response.status_code == 204
    
    # 7. Verify deletion
    verify_response = client.get(f"/products/{product_id}", headers=headers)
    assert verify_response.status_code == 404
