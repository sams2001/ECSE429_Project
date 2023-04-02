import pytest
import requests
import psutil
import os
from time import sleep

"""
Run tests with `pytest --durations=0 todos_tests.py` to see the duration of each test
"""

todos_url = 'http://localhost:4567/todos'

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
json_header = {"Content-Type": "application/json"}

"""
create, delete or change todo object at different states
"""

@pytest.fixture
def todos_setup_empty(resource):
    todos = requests.get(todos_url).json()['todos']
    while(len(todos) != 1):
        for i in range(1,len(todos)): #delete all but one.. basically empty
            todo = todos[i]
            request = requests.delete(todos_url + "/" + todo['id'])
        todos = requests.get(todos_url).json()['todos']
    assert len(requests.get(todos_url).json()['todos']) == 1


def populate_helper(num_to_reach):
    todos = requests.get(todos_url).json()['todos']
    num_todos = len(todos)
    while(len(todos) != num_to_reach):
        if (num_todos>num_to_reach):
            for i in range(num_todos-num_to_reach): 
                todo = todos[i]
                request = requests.delete(todos_url + "/" + todo['id'])
        else:
            for i in range(num_to_reach-num_todos):
                response = requests.post(todos_url,data=json_payload_todos,headers=json_header)
        todos = requests.get(todos_url).json()['todos']

    assert len(todos) == num_to_reach


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
def test_post_todos(resource, state):
    process = psutil.Process(os.getpid())
    response = requests.post(todos_url,data=json_payload_todos,headers=json_header)
    print('The CPU usage is: ', process.cpu_percent(0.5))
    print('RAM Used (GB):', str(process.memory_info().rss))

    assert response.status_code == 201
    sleep(0.1) #cpu takes 0.5s sample - make sure there's no overlap with other function calls


@pytest.mark.parametrize('state', ['todos_setup_very_populated', 'todos_setup_populated', 'todos_setup_half_populated', 'todos_setup_empty'])
def test_delete_todos(resource,state):
    process = psutil.Process(os.getpid())
    todos = requests.get(todos_url).json()['todos']
    todo_id = todos[0]['id']
    delete = requests.delete(todos_url + "/" + todo_id)
    print('The CPU usage is: ', process.cpu_percent(0.5))
    print('RAM Used (GB):', str(process.memory_info().rss))

    assert delete.status_code == 200
    sleep(0.1) #cpu takes 0.5s sample - make sure there's no overlap with other function calls


@pytest.mark.parametrize('state', ['todos_setup_very_populated', 'todos_setup_populated', 'todos_setup_half_populated', 'todos_setup_empty'])
def test_update_todos(resource,state):
    process = psutil.Process(os.getpid())
    todos = requests.get(todos_url).json()['todos']
    todo_id = todos[0]['id']
    update = requests.put(todos_url + '/' + todo_id,data=json_payload_todos_new,headers=json_header)
    print('The CPU usage is: ', process.cpu_percent(0.5))
    print('RAM Used (GB):', str(process.memory_info().rss))

    assert update.status_code == 200
    sleep(0.1)
