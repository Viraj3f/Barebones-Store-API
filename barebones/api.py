import bcrypt
from flask import request, jsonify

from app import app, db
from model import Producer, Product, ShoppingCart, ShoppingCartEntry


@app.route("/api/producer", methods=['POST'])
def producer():
    """
        POST: Creates a new producer.
    """
    content = request.get_json()
    username = content["username"]
    password = content["password"].encode('utf-8')

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    # Create a producer object and commit to the db
    producer = Producer(username=username, password=hashed_password)
    db.session.add(producer)
    db.session.commit()

    # Create the response message
    response = {
        "id": producer.id,
        "message": "New producer '{}' succesfully created".format(username)
    }

    return jsonify(response), 200


@app.route("/api/products", methods=['GET', 'POST'])
def products():
    """
        POST: Creates a new product in the store
        GET: Returns all products whose endpoint based on the number
             of availible products
    """
    if request.method == "POST":
        content = request.get_json()

        # Assert that price is greater than 1 cent
        assert content["price"] >= 0.1

        # Assert that the inventory count is not negative
        assert content["inventory_count"] >= 0

        # Crete a product object and commit ot db
        product = Product(
                producer_id=content["producer_id"],
                title=content["title"],
                price=content["price"],
                inventory_count=content["inventory_count"])

        db.session.add(product)
        db.session.commit()

        response = {
            "id": product.id,
            "message":
                "New product successfully created: {}".format(
                    product.__dict__)
        }

        return jsonify(response), 200

    elif request.method == "GET":
        print('gottem')
        pass
    else:
        print('nana')
        return "", 404


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
