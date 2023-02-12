import pytest
import requests
import json
import subprocess

url = 'http://localhost:4567/todos'


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
    new_todo_json = json.dumps({
        "title": "submit paperwork",
        "doneStatus": False,
        "description": ""
        })
    response = requests.post(url,data=new_todo_json,headers={"Content-Type": "application/json"})
    assert response.status_code == 201 #Create
    todos = requests.get(url).json()["todos"]
    assert response.json() in todos

def test_get_todos():
    response = requests.get(url+'/1')
    assert response.status_code == 200
    assert 'todos' in response.json()

def test_get_todos():
    response = requests.get(url+'/0')
    assert response.status_code == 404
    assert 'errorMessages' in response.json()

def test_delete_todo():
    r = requests.delete(url + "/1")
    assert r.status_code == 200

def test_delete_todo_failure():
    r = requests.delete(url + "/1000")
    assert r.status_code == 404