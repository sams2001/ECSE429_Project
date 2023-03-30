import pytest
import requests

#Run tests with `pytest --durations=0 todos_tests.py` to see the duration of each test

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

#empty state setup
@pytest.mark.order(1)
def todos_setup_empty(self, resource):
    while(1):
        todos = requests.get(todos_url).json()['todos']
        for i in range(1,len(todos)): #delete all but one.. basically empty
            todo = todos[i]
            request = requests.delete(todos_url + "/" + todo['id'])
        todos_after_delete = requests.get(todos_url).json()['todos']
        if len(todos_after_delete.json()['todos']) == 1:
            break


#empty state tests
@pytest.mark.order(2)
def test_post_todos(resource):
    response = requests.post(todos_url,data=json_payload_todos,headers=json_header)
    assert response.status_code == 201


@pytest.mark.order(3)
def test_delete_todos(resource):
    todos = requests.get(todos_url).json()['todos']
    todo_id = todos[0]['id']
    delete = requests.delete(todos_url + "/" + todo_id)
    assert delete.status_code == 200


@pytest.mark.order(4)
def test_update_todos(resource):
    todos = requests.get(todos_url).json()['todos']
    todo_id = todos[0]['id']
    update = requests.put(todos_url + '/' + todo_id,data=json_payload_todos_new,headers=json_header)
    assert update.status_code == 200


#half full state setup
@pytest.mark.order(5)
def todos_setup_half_populated(self, resource):
    for i in range(50):
        response = requests.post(todos_url,data=json_payload_todos,headers=json_header)
        assert response.status_code == 201 

#half full state tests
@pytest.mark.order(6)
def test_update_todos_half_populated(resource):
    test_update_todos(resource)

@pytest.mark.order(7)
def test_delete_todos_half_populated(resource):
    test_delete_todos(resource)

@pytest.mark.order(8)
def test_post_todos_half_populated(resource):
    test_post_todos(resource)


#full state setup
@pytest.mark.order(9)
def todos_setup_populated(self, resource):
    for i in range(100):
        response = requests.post(todos_url,data=json_payload_todos,headers=json_header)
        assert response.status_code == 201 


#half full state tests
@pytest.mark.order(10)
def test_update_todos_populated(resource):
    test_update_todos(resource)

@pytest.mark.order(11)
def test_delete_todos_populated(resource):
    test_delete_todos(resource)

@pytest.mark.order(12)
def test_post_todos_populated(resource):
    test_post_todos(resource)
