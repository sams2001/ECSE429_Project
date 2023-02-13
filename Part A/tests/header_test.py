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
        "title": "School",
        "description": "testing"
        })
    response = requests.post('http://localhost:4567/categories',data=new_category_json,headers={"Content-Type": "application/json"})
    assert response.status_code == 201 #Create
    categories = requests.get('http://localhost:4567/categories').json()["categories"]
    assert response.json() in categories


### GET BY ID ###

def test_get_todos():
    response = requests.get('http://localhost:4567/todos/1')
    assert response.status_code == 200
    assert 'todos' in response.json()

def test_get_projects():
    response = requests.get('http://localhost:4567/projects/1')
    assert response.status_code == 200
    assert 'projects' in response.json()

def test_get_categories():
    response = requests.get('http://localhost:4567/categories/1')
    assert response.status_code == 200
    assert 'categories' in response.json()


### GET BY NON-EXISTENT ID ###

def test_get_todos():
    response = requests.get('http://localhost:4567/todos/0')
    assert response.status_code == 404
    assert 'errorMessages' in response.json()

def test_get_projects():
    response = requests.get('http://localhost:4567/projects/0')
    assert response.status_code == 404
    assert 'errorMessages' in response.json()

def test_get_categories():
    response = requests.get('http://localhost:4567/categories/0')
    assert response.status_code == 404
    assert 'errorMessages' in response.json()


### CATEGORY & TODO RELATIONSHIP ###

def test_get_todos_by_category():
    response = requests.get('http://localhost:4567/categories/1/todos')
    todos = requests.get('http://localhost:4567/todos').json()["todos"]
    todos_in_category = [i for i in todos if 'categories' in i.keys() and {'id': '1'} in i['categories']]
    
    assert response.status_code == 200

    #from the original entries, todo 1 is in category 1 and todo 2 is not.
    print(requests.get('http://localhost:4567/todos/1').json()["todos"])
    print(todos_in_category)
    assert requests.get('http://localhost:4567/todos/1').json()["todos"][0] in todos_in_category
    assert requests.get('http://localhost:4567/todos/2').json()["todos"][0] not in todos_in_category


def test_get_categories_by_todos():
    response = requests.get('http://localhost:4567/todos/1/categories').json()["categories"]
    category = requests.get('http://localhost:4567/categories/1').json()["categories"][0]
    #from the original entries, todo 1 has category 1. if more categories are added, 
    # should still be valid, so just check that category 1 is still in todo 1's categories, not if they are equal
    assert category in response