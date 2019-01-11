"""
Defintion and handling of API endpoints.
"""

import bcrypt
from flask import request, jsonify

from barebones import app, db
from barebones.model import Producer, Product, ShoppingCart


@app.route("/api/producer", methods=['POST', 'GET'])
def producers():
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

        # Create JWT token
        response = {
            "producer": producer.as_dict(),
            "auth_token": producer.get_jwt_token().decode('utf-8')
        }

        return jsonify(response), 200
    elif request.method == "GET":
        producers = []
        for producer in Producer.query.all():
            producers.append(producer.as_dict())

        return jsonify({"products": producers}), 200


@app.route("/api/producer/<int:producer_id>", methods=['GET'])
def producer(producer_id):
    """
        GET: Gets a producer and their products.
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
        token = get_jwt_from_request(request)
        content = request.get_json()

        # Check that the producer id corresponds to an actual
        # producer in the db.
        assert type(content["producer_id"]) == int

        if not authorize_producer(content["producer_id"], token):
            return "", 401

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
        min_inventory_count = 1
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
        token = get_jwt_from_request(request)
        content = request.get_json()
        if not authorize_producer(content["producer_id"], token):
            return "", 401

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
        token = get_jwt_from_request(request)
        content = request.get_json()
        if not authorize_producer(content["producer_id"], token):
            return "", 401

        db.session.delete(product)
        db.session.commit()
        return jsonify({
            "message": "Deleted product with id: '{}'".format(product_id)
        }), 200


@app.route("/api/shopping_cart", methods=['POST'])
def shopping_carts():
    """
        POST: Create a new shopping cart
    """
    shopping_cart = ShoppingCart(cached_price=0)
    db.session.add(shopping_cart)
    db.session.commit()

    response = {
        "auth_token": shopping_cart.get_jwt_token().decode('utf-8'),
        "shopping_cart": shopping_cart.as_dict()
    }

    return jsonify(response), 200


@app.route("/api/shopping_cart/<int:shopping_cart_id>",
           methods=['GET', 'PUT', 'DELETE'])
def shopping_cart(shopping_cart_id):
    """
        GET: Return a specific shopping cart
        PUT: Update the shopping cart
        DELETE: Delete the shopping cart
    """
    shopping_cart = ShoppingCart.query.get(shopping_cart_id)
    content = request.get_json()
    token = get_jwt_from_request(request)

    if shopping_cart is None:
        return jsonify({}), 404

    if not shopping_cart.verify_jwt_token(token):
        return "", 401

    if request.method == "GET":
        arg = request.args.get('use-cache')
        if arg and int(arg) == 0:
            shopping_cart.recalculate_price()
        db.session.commit()

        return jsonify(shopping_cart.as_dict()), 200
    elif request.method == "DELETE":
        # Delete the shopping cart
        db.session.delete(shopping_cart)
        db.session.commit()
        return jsonify({
            "message": "Deleted shopping with id: '{}'"
            .format(shopping_cart_id)
        }), 200

    elif request.method == "PUT":
        assert "product_id" in content
        assert "quantity" in content

        # Find the associated product to add or modify in shopping cart
        product = Product.query.get(content["product_id"])
        if product is None:
            return {"message": "Product not found"}, 404

        shopping_cart.create_or_modify_shopping_cart_entry(
                product,
                content["quantity"])

        db.session.commit()

        return jsonify(shopping_cart.as_dict()), 200


@app.route("/api/shopping_cart/<int:shopping_cart_id>/checkout",
           methods=['POST'])
def checkout(shopping_cart_id):
    """
        POST: Checkout a shopping cart
    """
    shopping_cart = ShoppingCart.query.get(shopping_cart_id)
    token = get_jwt_from_request(request)

    if shopping_cart is None:
        return jsonify({"message": "Shopping card not found."}), 404

    if not shopping_cart.verify_jwt_token(token):
        return "", 401

    shopping_cart.recalculate_price()
    total_price = shopping_cart.cached_price
    for entry in shopping_cart.shopping_cart_entries:
        product_id = entry.product_id

        # Lock the product table
        product = db.session \
            .query(Product) \
            .filter(Product.id == product_id) \
            .with_for_update().one()

        if product is None:
            db.session.rollback()
            return jsonify({"message": "Missing product"}), 400

        if product.inventory_count < entry.quantity:
            db.session.rollback()
            return jsonify({"message": "Product out of stock."}), 400

        product.inventory_count -= entry.quantity

    db.session.commit()

    # Clean up shopping cart resources
    for entry in shopping_cart.shopping_cart_entries:
        db.session.delete(entry)

    db.session.delete(shopping_cart)
    db.session.commit()

    return jsonify({
                "message": "Products ordered, ${} spent"
                .format(total_price)
            }), 200


@app.route("/")
def welcome():
    # Simple welcome message for debugging
    return "Hello!"


def get_jwt_from_request(request):
    print(request.headers)
    auth = request.headers['Authorization'].split(" ")
    assert len(auth) == 2
    assert auth[0] == "Bearer"
    return auth[1]


def authorize_producer(producer_id, token):
    producer = Producer.query.get(producer_id)
    if producer is None:
        return False

    if not producer.verify_jwt_token(token):
        return False

    return True
