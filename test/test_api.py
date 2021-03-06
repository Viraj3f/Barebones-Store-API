import pytest
import json
import os
import tempfile

import sys
sys.path.append("..")
from barebones import app, db # noqa


@pytest.fixture
def client():
    tmp_fd, tmp = tempfile.mkstemp()

    TEST_DATABASE_URI = "sqlite:///" + tmp
    app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI

    client = app.test_client()
    db.create_all()

    yield client

    os.close(tmp_fd)
    os.remove(tmp)


"""
Helper methods
"""


def create_producer(client, username, password):
    return client.post(
            '/api/producer',
            data=json.dumps({
                "username": username,
                "password": password,
            }),
            content_type='application/json')


def create_auth_header(token):
    return {
        "Authorization": "Bearer {}".format(token)
    }


def create_product(
        client, token, title, inventory_count, price, producer_id):

    return client.post(
            '/api/products',
            headers=create_auth_header(token),
            data=json.dumps({
                "title": title,
                "producer_id": producer_id,
                "inventory_count": inventory_count,
                "price": price
            }),
            content_type='application/json')


"""
Integration tests
"""


def test_root(client):
    # Simple test to see if server is working
    response = client.get('/')
    assert response.data == b"Hello!"


def test_create_producer(client):
    response = create_producer(client, "uname", "password")
    assert response.status_code == 200
    content = response.get_json()
    assert content["producer"]["username"] == "uname"

    created = \
        client.get('/api/producer/' + str(content["producer"]["id"])) \
        .get_json()
    assert created["id"] == content["producer"]["id"]
    assert created["username"] == content["producer"]["username"]


def test_create_product(client):
    response = create_producer(client, "uname1", "password")
    producer1 = response.get_json()
    assert producer1["producer"]["id"] == 1

    response = create_producer(client, "uname2", "password")
    producer2 = response.get_json()
    assert producer2["producer"]["id"] == 2

    assert 200 == create_product(
            client,
            producer1["auth_token"],
            "prod1", 11, 100,
            producer1["producer"]["id"]).status_code
    assert 200 == create_product(
            client,
            producer2["auth_token"],
            "prod2a", 13, 42,
            producer2["producer"]["id"]).status_code
    assert 200 == create_product(
            client,
            producer2["auth_token"],
            "prod2b", 14, 86,
            producer2["producer"]["id"]).status_code
    assert 401 == create_product(
            client,
            "",
            "stub", 10, 31,
            991).status_code

    body = client.get('/api/products').get_json()
    assert len(body["products"]) == 3

    body = client.get('/api/products?min-inventory-count=12').get_json()
    assert len(body["products"]) == 2

    body = client.get('/api/products?min-inventory-count=14').get_json()
    assert len(body["products"]) == 1

    body = client.get('/api/products?min-inventory-count=99').get_json()
    assert len(body["products"]) == 0


def test_shopping_cart(client):
    response = client.post('/api/shopping_cart')
    assert response.status_code == 200
    token = response.get_json()["auth_token"]
    cart = response.get_json()["shopping_cart"]

    created = \
        client.get('/api/shopping_cart/' + str(cart["id"]),
                   headers=create_auth_header(token)) \
        .get_json()

    assert cart["id"] == created["id"]

    client.delete('/api/shopping_cart/' + str(cart["id"]),
                  headers=create_auth_header(token))

    assert client.get(
            '/api/shopping_cart/' + str(cart["id"]),
            headers=create_auth_header(token)).status_code == 404


def test_checkout(client):
    # Create producer
    producer = create_producer(client, "uname", "password").get_json()

    # Create Products
    p1 = create_product(
            client,
            producer["auth_token"],
            "p1", 10, 100,
            producer["producer"]["id"]).get_json()
    p2 = create_product(
            client,
            producer["auth_token"],
            "p2", 17, 200,
            producer["producer"]["id"]).get_json()

    # Create shopping cart
    response = client.post('/api/shopping_cart').get_json()
    token = response["auth_token"]
    cart = response["shopping_cart"]

    # Add to cart
    client.put(
            '/api/shopping_cart/' + str(cart["id"]),
            data=json.dumps({
                    "product_id": p1["id"],
                    "quantity": 3
                }),
            headers=create_auth_header(token),
            content_type='application/json')

    client.put(
            '/api/shopping_cart/' + str(cart["id"]),
            data=json.dumps({
                    "product_id": p2["id"],
                    "quantity": 1
                }),
            headers=create_auth_header(token),
            content_type='application/json')

    cart = client.get(
            '/api/shopping_cart/' + str(cart["id"]),
            headers=create_auth_header(token)
            ).get_json()
    assert cart["cached_price"] == 500

    client.put(
            '/api/shopping_cart/' + str(cart["id"]),
            data=json.dumps({
                    "product_id": p1["id"],
                    "quantity": 1
                }),
            headers=create_auth_header(token),
            content_type='application/json')

    cart = client.get(
            '/api/shopping_cart/' + str(cart["id"]),
            headers=create_auth_header(token),
            ).get_json()
    assert cart["cached_price"] == 300

    client.put(
            '/api/shopping_cart/' + str(cart["id"]),
            data=json.dumps({
                    "product_id": p1["id"],
                    "quantity": 0
                }),
            headers=create_auth_header(token),
            content_type='application/json')

    cart = client.get(
            '/api/shopping_cart/' + str(cart["id"]),
            headers=create_auth_header(token),
            ).get_json()
    assert cart["cached_price"] == 200

    client.post(
            '/api/shopping_cart/' + str(cart["id"]) + '/checkout',
            headers=create_auth_header(token),
            )
    p2 = client.get('/api/products/' + str(p2["id"])).get_json()

    assert p2["inventory_count"] == 16
