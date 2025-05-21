import requests

BASE_URL = "http://localhost:5000"

def test_get_products():
    r = requests.get(f"{BASE_URL}/products")
    print("GET /products:", r.json())

def test_add_product():
    new_product = {"name": "Tablet", "price": 300}
    r = requests.post(f"{BASE_URL}/products", json=new_product)
    print("POST /products:", r.json())

def test_update_product():
    updated_data = {"price": 350}
    r = requests.put(f"{BASE_URL}/products/3", json=updated_data)
    print("PUT /products/3:", r.json())

def test_delete_product():
    r = requests.delete(f"{BASE_URL}/products/3")
    print("DELETE /products/3:", r.status_code)

if __name__ == "__main__":
    test_get_products()
    test_add_product()
    test_get_products()
    test_update_product()
    test_get_products()
    test_delete_product()
    test_get_products()
