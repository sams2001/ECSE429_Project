import pytest
import requests
import os
import psutil
import json
from time import sleep

url = 'http://localhost:4567/'

json_payload_todos = """
    {
        "title": "submit paperwork",
        "doneStatus": False,
        "description": ""
    }
    """

json_payload_todos_new = """
    {
        "title": "delete paperwork",
        "doneStatus": False,
        "description": ""
    }
    """

json_payload_categories = """{
        "title": "School",
        "description": "testing"
        }"""
json_payload_categories_new = """{
        "title": "School",
        "description": "testing"
        }"""
json_payload_projects = """
{
    "title": "Home Activities",
    "completed": False,
    "active": False,
    "description": ""
}"""
json_payload_projects_new = """
{
    "title": "Work Activities",
    "completed": False,
    "active": False,
    "description": ""
}"""

json_header = {"Content-Type": "application/json"}

"""
create, delete or change relationships between categories, projects, and todos at different states
"""
@pytest.fixture
def todos_setup_empty(resource):
    todos = requests.get('http://localhost:4567/todos').json()['todos']
    while(len(todos) != 1):
        for i in range(1,len(todos)): #delete all but one.. basically empty
            todo = todos[i]
            request = requests.delete('http://localhost:4567/todos' + "/" + todo['id'])
        todos = requests.get('http://localhost:4567/todos').json()['todos']

def populate_helper(num_to_reach):
    todos = requests.get('http://localhost:4567/todos').json()['todos']
    num_todos = len(todos)
    while(len(todos) != num_to_reach):
        if (num_todos>num_to_reach):
            for i in range(num_todos-num_to_reach): 
                todo = todos[i]
                request = requests.delete('http://localhost:4567/todos' + "/" + todo['id'])
        else:
            for i in range(num_to_reach-num_todos):
                response = requests.post('http://localhost:4567/todos',data=json_payload_todos,headers=json_header)
        todos = requests.get('http://localhost:4567/todos').json()['todos']

@pytest.fixture
def todos_setup_half_populated(resource):
    populate_helper(50)
@pytest.fixture
def todos_setup_populated(resource):
    populate_helper(100) 
@pytest.fixture
def todos_setup_very_populated(resource):
    populate_helper(500)

@pytest.mark.parametrize('state', ['todos_setup_very_populated', 'todos_setup_populated', 'todos_setup_half_populated', 'todos_setup_empty'])
#add a category to a todo
def test_post_category_to_todo(resource,state):
    post = requests.post(url+"todos",data=json_payload_todos,headers=json_header)
    id_todo = post.json()["id"]
    post2 = requests.post(url+"categories",data=json_payload_categories,headers=json_header)
    id_category = post2.json()["id"]
    json_body = json.dumps({
        "id": f"{id_category}",
        })
    process = psutil.Process(os.getpid())
    print('The CPU usage is: ', psutil.cpu_percent(0.5))
    response = requests.post("http://localhost:4567/todos/"+id_todo+"/categories", data=json_body, headers=json_header)
    print('RAM Used (GB):', str(process.memory_info().rss))
    assert response.status_code == 201
    sleep(0.1)

@pytest.mark.parametrize('state', ['todos_setup_very_populated', 'todos_setup_populated', 'todos_setup_half_populated', 'todos_setup_empty'])
#add a todo to a category 
def test_post_todo_to_category(resource,state):
    post = requests.post(url+"todos",data=json_payload_todos,headers=json_header)
    id_todo = post.json()["id"]
    post2 = requests.post(url+"categories",data=json_payload_categories,headers=json_header)
    id_category = post2.json()["id"]
    json_body = json.dumps({
        "id": f"{id_todo}",
        })
    process = psutil.Process(os.getpid())
    print('The CPU usage is: ', psutil.cpu_percent(0.5))
    response = requests.post("http://localhost:4567/categories/"+id_category+"/todos", data=json_body, headers=json_header)
    print('RAM Used (GB):', str(process.memory_info().rss))
    assert response.status_code == 201
    sleep(0.1)

@pytest.mark.parametrize('state', ['todos_setup_very_populated', 'todos_setup_populated', 'todos_setup_half_populated', 'todos_setup_empty'])
#delete category from todo
def test_delete_category_from_todo(resource,state):
    post = requests.post(url+"todos",data=json_payload_todos,headers=json_header)
    id_todo = post.json()["id"]
    post2 = requests.post(url+"categories",data=json_payload_categories,headers=json_header)
    id_category = post2.json()["id"]
    json_body = json.dumps({
        "id": f"{id_category}",
        })
    post3 = requests.post("http://localhost:4567/todos/"+id_todo+"/categories", data=json_body, headers=json_header)
    process = psutil.Process(os.getpid())
    print('The CPU usage is: ', psutil.cpu_percent(0.5))
    response = requests.delete(url+ "todos/"+id_todo+"/categories/"+id_category)
    print('RAM Used (GB):', str(process.memory_info().rss))
    assert response.status_code == 200
    assert requests.get(url+ "todos/"+id_todo+"/categories/"+id_category).status_code == 404
    sleep(0.1)
@pytest.mark.parametrize('state', ['todos_setup_very_populated', 'todos_setup_populated', 'todos_setup_half_populated', 'todos_setup_empty'])
    #adding a category to a project
def test_post_category_to_project(resource,state):
    post = requests.post(url+"projects",data=json_payload_projects,headers=json_header)
    id_to_use = post.json()["id"]
    post2 = requests.post(url+"categories",data=json_payload_categories,headers=json_header)
    id_category = post2.json()["id"]    
    json_body = json.dumps({
    "id": f"{id_category}",
    })
    process = psutil.Process(os.getpid())
    print('The CPU usage is: ', psutil.cpu_percent(0.5))
    response = requests.post(url+"projects/"+id_to_use+"/categories", headers=json_header, data=json_body)
    print('RAM Used (GB):', str(process.memory_info().rss))
    assert response.status_code == 201
    sleep(0.2)