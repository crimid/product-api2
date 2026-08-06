import pytest
from tests.conftest import client, auth_headers, sample_product

@pytest.mark.benchmark
def test_create_product_performance(client, auth_headers, sample_product, benchmark):
    """Benchmark product creation performance."""
    def create_product():
        response = client.post("/products", json=sample_product, headers=auth_headers)
        assert response.status_code == 201
    
    result = benchmark(create_product)
    print(f"\nProduct creation benchmark: {result}")

@pytest.mark.benchmark
def test_list_products_performance(client, auth_headers, benchmark):
    """Benchmark listing products performance."""
    for i in range(10):
        product_data = {
            "name": f"Performance Product {i}",
            "description": f"Product {i} for performance testing",
            "price": 99.99 + i,
            "stock": 10 + i
        }
        client.post("/products", json=product_data, headers=auth_headers)
    
    def list_products():
        response = client.get("/products", headers=auth_headers)
        assert response.status_code == 200
    
    result = benchmark(list_products)
    print(f"\nProducts listing benchmark: {result}")

@pytest.mark.benchmark
def test_get_product_performance(client, auth_headers, sample_product, benchmark):
    """Benchmark getting a single product performance."""
    create_response = client.post("/products", json=sample_product, headers=auth_headers)
    product_id = create_response.json()["id"]
    
    def get_product():
        response = client.get(f"/products/{product_id}", headers=auth_headers)
        assert response.status_code == 200
    
    result = benchmark(get_product)
    print(f"\nGet product benchmark: {result}")

@pytest.mark.benchmark
def test_auth_performance(client, test_user, benchmark):
    """Benchmark authentication performance."""
    client.post("/register", json=test_user)
    
    def login():
        response = client.post(
            "/login",
            data={
                "username": test_user["username"],
                "password": test_user["password"]
            }
        )
        assert response.status_code == 200
    
    result = benchmark(login)
    print(f"\nAuthentication benchmark: {result}")
