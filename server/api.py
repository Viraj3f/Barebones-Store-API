from model import Products
from app import app, db


@app.route("/api/products", methods=['GET', 'POST'])
def products():
    """
        POST: Creates a new product in the store
        GET: Returns all products whose endpoint based on the number
             of availible products
    """
    return "hello!"


@app.route("/api/products/<int:product_id>", methods=['GET', 'PUT', 'DELETE'])
def product(product_id):
    """
        GET: Returns the serialized information about a particular product
        PUT: Updates the information about a particular product to match
             a new schema.
        DELETE: Deletes a product.
    """
    return "hello!"


@app.route("/api/shopping_carts/", methods=['POST'])
def shopping_carts():
    """
        POST: Create a new shopping cart
    """
    return "Hello!"


@app.route("/api/shopping_carts/<int:shopping_cart_id>",
           methods=['GET', 'PUT'])
def shopping_cart():
    """
        GET: Return a specific shopping cart
        PUT: Update the shopping cart
    """
    return "Hello!"


@app.route("/api/checkout/<int:shopping_cart_id>", methods=['POST'])
def checkout():
    """
        GET: Return a specific shopping cart
        PUT: Update the shopping cart
    """
    return "Hello!"
