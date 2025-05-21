from flask import Blueprint, jsonify, request

products_bp = Blueprint('products', __name__, url_prefix='/products')

# In-memory list of products (simulate DB)
products = [
    {"id": 1, "name": "Apple", "price": 1.5},
    {"id": 2, "name": "Banana", "price": 0.75},
]

@products_bp.route('/', methods=['GET'])
def get_products():
    return jsonify(products)

@products_bp.route('/', methods=['POST'])
def add_product():
    new_product = request.json
    new_product["id"] = products[-1]["id"] + 1 if products else 1
    products.append(new_product)
    return jsonify(new_product), 201

@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    updated_product = request.json
    for p in products:
        if p["id"] == product_id:
            p.update(updated_product)
            return jsonify(p)
    return jsonify({"error": "Product not found"}), 404

@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p["id"] != product_id]
    return jsonify({"message": "Product deleted"})
