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
"""
# need to figure out how to run each set up then run each test 


    def todos_setup_empty(self, resource):
        while(1):
            todos = requests.get(todos_url).json()['todos']
            for i in range(1,len(todos)): #delete all but one.. basically empty
                todo = todos[i]
                request = requests.delete(todos_url + "/" + todo['id'])
            todos_after_delete = requests.get(todos_url).json()['todos']
            if len(todos_after_delete.json()['todos']) == 1:
                break

    def todos_setup_populated(self, resource):
        for i in range(50):
            response = requests.post(todos_url,data=json_payload_todos,headers=json_header)
            assert response.status_code == 201 

    def todos_setup_populated(self, resource):
        for i in range(100):
            response = requests.post(todos_url,data=json_payload_todos,headers=json_header)
            assert response.status_code == 201 
"""

def test_post_todos(resource):
    response = requests.post(todos_url,data=json_payload_todos,headers=json_header)
    assert response.status_code == 201

def test_delete_todos(resource):
    todos = requests.get(todos_url).json()['todos']
    todo_id = todos[0]['id']
    delete = requests.delete(todos_url + "/" + todo_id)
    assert delete.status_code == 200

def test_update_todo(resource):
    todos = requests.get(todos_url).json()['todos']
    todo_id = todos[0]['id']
    update = requests.put(todos_url + '/' + todo_id,data=json_payload_todos_new,headers=json_header)
    assert update.status_code == 200