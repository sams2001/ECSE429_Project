import pytest
import requests
import json
import subprocess

#initial state restored once app is terminated
@pytest.fixture(scope="session", autouse=True)
def kill_app():
    try:
        process = subprocess.call(['curl', 'http://localhost:4567/shutdown'], shell=True)
    except ConnectionError:
        pass
    

@pytest.fixture(scope='module')
def start_app():
    process =  subprocess.Popen(["java", "-jar", "runTodoManagerRestAPI-1.5.5.jar"], shell=True)
    status_code = subprocess.call(['curl', 'http://localhost:4567'], shell=True)
    while status_code:
        status_code = subprocess.call(['curl', 'http://localhost:4567'], shell=True)
    yield status_code
    kill_app()


##### HEADERS ####

def test_header():
    response = requests.get('http://localhost:4567')
    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'text/html'


### GET ###

def test_get_todos():
    response = requests.get('http://localhost:4567/todos')
    assert response.status_code == 200
    assert 'todos' in response.json()

def test_get_projects():
    response = requests.get('http://localhost:4567/projects')
    assert response.status_code == 200
    assert 'projects' in response.json()

def test_get_categories():
    response = requests.get('http://localhost:4567/categories')
    assert response.status_code == 200
    assert 'categories' in response.json()