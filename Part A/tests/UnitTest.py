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

def test_todos_header():
    response = requests.head('http://localhost:4567/todos')
    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json'

def test_categories_header():
    response = requests.head('http://localhost:4567/categories')
    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json'

def test_projects_header():
    response = requests.head('http://localhost:4567/projects')
    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json'

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


### POST ###

def test_post_todos_json():
    new_todo_json = json.dumps({
        "title": "submit paperwork",
        "doneStatus": False,
        "description": ""
        })
    response = requests.post('http://localhost:4567/todos',data=new_todo_json,headers={"Content-Type": "application/json"})
    assert response.status_code == 201 #Create
    todos = requests.get('http://localhost:4567/todos').json()["todos"]
    assert response.json() in todos


def test_post_project_json():
    new_project_json = json.dumps({
        "title": "Home Activities",
        "completed": False,
        "active": False,
        "description": ""
        })
    response = requests.post('http://localhost:4567/projects',data=new_project_json,headers={"Content-Type": "application/json"})
    assert response.status_code == 201 #Create
    projects = requests.get('http://localhost:4567/projects').json()["projects"]
    assert response.json() in projects


def test_post_category_json():
    new_category_json = json.dumps({
        "title": "Extracurricular",
        "description": ""
        })
    response = requests.post('http://localhost:4567/categories',data=new_category_json,headers={"Content-Type": "application/json"})
    assert response.status_code == 201 #Create
    categories = requests.get('http://localhost:4567/categories').json()["categories"]
    assert response.json() in categories

### GET BY ID ###

