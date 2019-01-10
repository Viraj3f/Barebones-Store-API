"""
Defintion and handling of API endpoints.
"""

import bcrypt
from flask import request, jsonify

from app import app, db
from model import Producer, Product, ShoppingCart, ShoppingCartEntry


@app.route("/api/producer", methods=['POST', 'GET'])
def producer():
    """
        POST: Creates a new producer.
    """
    if request.method == "POST":
        content = request.get_json()
        username = content["username"]
        password = content["password"].encode('utf-8')

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        # Create a producer object and commit to the db
        producer = Producer(username=username, password=hashed_password)
        db.session.add(producer)
        db.session.commit()

        return jsonify(producer.as_dict()), 200
    elif request.method == "GET":
        producers = []
        for producer in Producer.query.all():
            producers.append(producer.as_dict())

        return jsonify({"products": producers}), 200


@app.route("/api/producer/<int:producer_id>", methods=['GET'])
def producer_get(producer_id):
    """
        GET: Creates a new producer.
    """
    producer = Producer.query.get(producer_id)

    if producer is None:
        return jsonify({}), 404

    return jsonify(producer.as_dict()), 200


@app.route("/api/products", methods=['GET', 'POST'])
def products():
    """
        POST: Creates a new product in the store
        GET: Returns all products whose endpoint based on the number
             of availible products
    """
    if request.method == "POST":
        content = request.get_json()

        # Check that the producer id corresponds to an actual
        # producer in the db.
        assert type(content["producer_id"]) == int
        producer = Producer.query.get(content["producer_id"])
        if producer is None:
            return jsonify({"message": "Producer id does not exist"}), 401

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
                    product.as_dict())
        }

        return jsonify(response), 200

    elif request.method == "GET":
        # Select matchin prodcuts whose inventory is greater than a specified
        # minimum value.
        arg = request.args.get('min-inventory-count')
        min_inventory_count = 0
        if arg is not None:
            min_inventory_count = int(arg)
        filtered = Product \
            .query \
            .filter(
                Product.inventory_count >= min_inventory_count)

        matching_products = []
        for match in filtered:
            matching_products.append(match.as_dict())

        return jsonify({"products": matching_products}), 200


@app.route("/api/products/<int:product_id>", methods=['GET', 'PUT', 'DELETE'])
def product(product_id):
    """
        GET: Returns the serialized information about a particular product
        PUT: Updates the information about a particular product to match
             a new schema.
        DELETE: Deletes a product.
    """
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({}), 404

    if request.method == "GET":
        # Return the product recor
        return jsonify(product.as_dict()), 200
    elif request.method == "PUT":
        content = request.get_json()
        if "title" in content:
            product.title = content["title"]
        if "price" in content:
            product.price = content["price"]
        if "inventory_count" in content:
            product.inventory_count = content["inventory_count"]
        db.session.commit()

        # Return the modified product recor
        return jsonify(product.as_dict()), 200
    elif request.method == "DELETE":
        db.session.delete(product)
        db.session.commit()
        return jsonify({
            "message": "Deleted product with id: '{}'".format(product_id)
        }), 200


@app.route("/api/shopping_carts/", methods=['POST'])
def shopping_carts():
    """
        POST: Create a new shopping cart
    """
    shopping_cart = ShoppingCart(cached_price=0)
    return jsonify(shopping_cart.as_dict()), 200


@app.route("/api/shopping_carts/<int:shopping_cart_id>",
           methods=['GET', 'PUT'])
def shopping_cart(shopping_cart_id):
    """
        GET: Return a specific shopping cart
        PUT: Update the shopping cart
    """
    if request.method == "GET":
        shopping_cart = ShoppingCart.query.get(shopping_cart_id)
        if shopping_cart is None:



    elif request.method == "POST":
        pass


@app.route("/api/checkout/<int:shopping_cart_id>", methods=['POST'])
def checkout():
    """
        GET: Return a specific shopping cart
        PUT: Update the shopping cart
    """
    return "Hello!"
