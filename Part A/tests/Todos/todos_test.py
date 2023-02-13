import pytest
import requests
import json
import subprocess

url = 'http://localhost:4567/todos'

json_payload = """
{
    "title": "submit paperwork",
    "doneStatus": False,
    "description": ""
}
"""

json_incorrect_payload = """
{
    "id": 10000,
    "title": "submit paperwork",
    "doneStatus": False,
    "description": ""
}
"""

json_header = {"Content-Type": "application/json"}


def test_todos_header():
    response = requests.head(url)
    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json'

def test_get_todos():
    response = requests.get(url)
    assert response.status_code == 200
    assert 'todos' in response.json()

def test_post_todos_json():
    response = requests.post(url,data=json_payload,headers=json_header)
    assert response.status_code == 201 #Create
    todos = requests.get(url).json()["todos"]
    assert response.json() in todos

def test_post_todos_faulty_json():
    response = requests.post(url,data=json_incorrect_payload,headers=json_header)
    assert response.status_code == 400  #Bad request
    assert 'Not allowed to create with id' in str(response.json())

def test_get_todo_by_id():
    response = requests.get(url+'/1')
    assert response.status_code == 200
    assert 'todos' in response.json()

def test_get_todos_by_id_dne():
    response = requests.get(url+'/0')
    assert response.status_code == 404
    assert 'errorMessages' in response.json()

def test_delete_todo():
    post = requests.post(url,data=json_payload,headers=json_header)
    id_to_delete = post.json()["id"]
    r = requests.delete(url + "/"+id_to_delete)
    assert r.status_code == 200

def test_delete_todo_failure():
    r = requests.delete(url + "/1000")
    assert r.status_code == 404