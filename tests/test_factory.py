from web_app import create_app

"""
Version: 1.0

Description:
Here we will do basic testing like app config and run finely.

Number of tests : 2

"""

def test_config():
    assert not create_app().testing # True when test conf not passed
    assert create_app({'TESTING': True}).testing # True if test conf passed


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, This project is working!'