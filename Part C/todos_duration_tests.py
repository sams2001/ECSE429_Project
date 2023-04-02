import pytest
import requests
import psutil
import os
from time import sleep

"""
Run tests with `pytest --durations=0 todos_duration_tests.py` to see the duration of each test
Install pytest-monitor 
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


def populate_helper(num_to_reach):
    __tracebackhide__ = True
    todos = requests.get(todos_url).json()['todos']
    num_todos = len(todos)
    while(len(todos) != num_to_reach):
        if (num_todos>num_to_reach):
            for i in range(0,num_todos-num_to_reach): 
                todo = todos[i]
                request = requests.delete(todos_url + "/" + todo['id'])
        else:
            for i in range(num_to_reach-num_todos):
                response = requests.post(todos_url,data=json_payload_todos,headers=json_header)
        todos = requests.get(todos_url).json()['todos']

    assert len(todos) == num_to_reach


@pytest.fixture
def todos_setup_empty(resource):
    populate_helper(1)

@pytest.fixture
def todos_setup_half_populated(resource):
    populate_helper(50)

@pytest.fixture
def todos_setup_populated(resource):
    populate_helper(100)

@pytest.fixture
def todos_setup_very_populated(resource):
    populate_helper(500)


#parameterizing fixtures causes errors
"""
post at different states
"""
def test_post_todos_empty(resource, todos_setup_empty):
    length = len(requests.get(todos_url).json()['todos'])
    response = requests.post(todos_url,data=json_payload_todos,headers=json_header)
    assert response.status_code == 201

def test_post_todos_half_populated(resource, todos_setup_half_populated):
    length = len(requests.get(todos_url).json()['todos'])
    response = requests.post(todos_url,data=json_payload_todos,headers=json_header)
    assert response.status_code == 201

def test_post_todos_populated(resource, todos_setup_populated):
    length = len(requests.get(todos_url).json()['todos'])
    response = requests.post(todos_url,data=json_payload_todos,headers=json_header)
    assert response.status_code == 201

def test_post_todos_very_populated(resource, todos_setup_very_populated):
    length = len(requests.get(todos_url).json()['todos'])
    response = requests.post(todos_url,data=json_payload_todos,headers=json_header)
    assert response.status_code == 201

"""
delete at different states
"""
def test_delete_todos_empty(resource,todos_setup_empty):
    todos = requests.get(todos_url).json()['todos']
    todo_id = todos[0]['id']
    delete = requests.delete(todos_url + "/" + todo_id)
    assert delete.status_code == 200
    
def test_delete_todos_half_populated(resource,todos_setup_half_populated):
    todos = requests.get(todos_url).json()['todos']
    todo_id = todos[0]['id']
    delete = requests.delete(todos_url + "/" + todo_id)
    assert delete.status_code == 200
    
def test_delete_todos_populated(resource,todos_setup_populated):
    todos = requests.get(todos_url).json()['todos']
    todo_id = todos[0]['id']
    delete = requests.delete(todos_url + "/" + todo_id)
    assert delete.status_code == 200

def test_delete_todos_very_populated(resource,todos_setup_very_populated):
    todos = requests.get(todos_url).json()['todos']
    todo_id = todos[0]['id']
    delete = requests.delete(todos_url + "/" + todo_id)
    assert delete.status_code == 200

"""
update at different states
"""
def test_update_todos_empty(resource,todos_setup_empty):
    todos = requests.get(todos_url).json()['todos']
    todo_id = todos[0]['id']
    update = requests.put(todos_url + '/' + todo_id,data=json_payload_todos_new,headers=json_header)
    assert update.status_code == 200
    
def test_update_todos_half_populated(resource,todos_setup_half_populated):
    todos = requests.get(todos_url).json()['todos']
    todo_id = todos[0]['id']
    update = requests.put(todos_url + '/' + todo_id,data=json_payload_todos_new,headers=json_header)
    assert update.status_code == 200

def test_update_todos_populated(resource,todos_setup_populated):
    todos = requests.get(todos_url).json()['todos']
    todo_id = todos[0]['id']
    update = requests.put(todos_url + '/' + todo_id,data=json_payload_todos_new,headers=json_header)
    assert update.status_code == 200

def test_update_todos_very_populated(resource,todos_setup_very_populated):
    todos = requests.get(todos_url).json()['todos']
    todo_id = todos[0]['id']
    update = requests.put(todos_url + '/' + todo_id,data=json_payload_todos_new,headers=json_header)
    assert update.status_code == 200


@pytest.mark.skip
def test_update_todos_helper(num_to_reach):
        __tracebackhide__ = True
        for i in range(num_to_reach):
            todo_id = requests.get(todos_url).json()['todos'][i]['id']
            update = requests.put(todos_url + '/' + todo_id,data=json_payload_todos_new,headers=json_header)
            assert update.status_code == 200

@pytest.mark.skip
def test_delete_todos_helper(num_to_reach):
    __tracebackhide__ = True
    for i in range(num_to_reach):
        todo_id = requests.get(todos_url).json()['todos'][0]['id']
        response = requests.delete(todos_url + "/" + todo_id)
        assert response.status_code == 200


"""
post varying amount of objects
"""
@pytest.mark.parametrize('num', ['1', '50', '100', '500'])
def test_post_num_todos(resource,todos_setup_empty,num):
    for i in range(int(num)):
        todo_id = requests.get(todos_url).json()['todos'][i]['id']
        response = requests.post(todos_url,data=json_payload_todos,headers=json_header)
        assert response.status_code == 201

"""
update varying amount of objects
"""
def test_update_1_todos(resource,todos_setup_empty):
    test_update_todos_helper(1)
def test_update_50_todos(resource,todos_setup_half_populated):
    test_update_todos_helper(50)
def test_update_100_todos(resource,todos_setup_populated):
    test_update_todos_helper(100)
def test_update_500_todos(resource,todos_setup_very_populated):
    test_update_todos_helper(500)
    


"""
delete varying amount of objects
"""
def test_delete_1_todos(resource,todos_setup_empty):
    test_delete_todos_helper(1)
def test_delete_50_todos(resource,todos_setup_half_populated):
    test_delete_todos_helper(50)
def test_delete_100_todos(resource,todos_setup_populated):
    test_delete_todos_helper(100)
def test_delete_500_todos(resource,todos_setup_very_populated):
    test_delete_todos_helper(500)
