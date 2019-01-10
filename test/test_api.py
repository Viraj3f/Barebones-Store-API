import pytest
import json

import sys
sys.path.append("..")
from run import app, db

TEST_DATABASE_URI = "sqlite:///./test.db"
TEST_SERVER_IP = "0.0.0.0"
app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
client = app.test_client()


def test_create_producer():
    print("ypyp")
    response = client.post(
            '/',
            data=json.dumps({
                "id": 1,
                "message": "New producer 'yoyo' succesfully created"
             }),
            content_type='application/json')
    print(response)
    assert False
