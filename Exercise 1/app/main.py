from flask import Flask
from .products import products_bp  # relative import

app = Flask(__name__)
app.register_blueprint(products_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
