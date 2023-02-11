import pytest
import requests
import json

##### HEADERS ####

def test_header():
    response = requests.get('http://localhost:4567')
    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'text/html'

