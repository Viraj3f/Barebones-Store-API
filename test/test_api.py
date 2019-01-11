import pytest
import json

import sys
sys.path.append("..")
from barebones.app import app

TEST_DATABASE_URI = "sqlite:///./test.db"
TEST_SERVER_IP = "0.0.0.0"
app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
client = app.test_client()


def test_create_producer():
    response = client.get('/')
    print(response)
    assert False
