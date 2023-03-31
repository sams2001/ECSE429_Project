import pytest
import requests
import os
import psutil
from time import sleep

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


def todos_setup_empty():
    todos = requests.get(todos_url).json()['todos']
    while(len(todos) != 1):
        for i in range(1,len(todos)): #delete all but one.. basically empty
            todo = todos[i]
            request = requests.delete(todos_url + "/" + todo['id'])
        todos = requests.get(todos_url).json()['todos']

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

    #assert len(todos) == num_to_reach


def todos_setup_half_populated():
    populate_helper(50)

def todos_setup_populated():
    populate_helper(100) 

def todos_setup_very_populated():
    populate_helper(500)


def test_control():
    print()
    print("==============================================================  Control  ===============================================================")
    process = psutil.Process(os.getpid())
    print('The CPU usage is: ', psutil.cpu_percent(0.5))
    print('RAM Used (GB):', str(process.memory_info().rss))


def test_post_todos():
    process = psutil.Process(os.getpid())
    print('The CPU usage is: ', psutil.cpu_percent(0.5))
    response = requests.post(todos_url,data=json_payload_todos,headers=json_header)
    print('RAM Used (GB):', str(process.memory_info().rss))
    assert response.status_code == 201
    sleep(0.2)


def test_delete_todos():
    process = psutil.Process(os.getpid())
    todos = requests.get(todos_url).json()['todos']
    todo_id = todos[0]['id']
    print('The CPU usage is: ', psutil.cpu_percent(0.5))
    delete = requests.delete(todos_url + "/" + todo_id)
    print('RAM Used (GB):', str(process.memory_info().rss))
    assert delete.status_code == 200
    sleep(0.2)


def test_update_todos():
    process = psutil.Process(os.getpid())
    todos = requests.get(todos_url).json()['todos']
    todo_id = todos[0]['id']
    print('The CPU usage is: ', psutil.cpu_percent(0.5))
    update = requests.put(todos_url + '/' + todo_id,data=json_payload_todos_new,headers=json_header)
    print('RAM Used (GB):', str(process.memory_info().rss))
    assert update.status_code == 200
    sleep(0.2)


if __name__ == "__main__":
    test_control()
    print()
    print("==============================================================  Empty  ===============================================================")
    todos_setup_empty()
    print("POST request:")
    test_post_todos()
    print()
    print("PUT request:")
    test_update_todos()
    print()
    print("DELETE request:")
    test_delete_todos() 
    
    print()
    print("============================================================  50 in system  ==============================================================")
    
    todos_setup_half_populated()
    print("POST request:")
    test_post_todos()
    print()
    print("PUT request:")
    test_update_todos()
    print()
    print("DELETE request:")
    test_delete_todos() 
    
    print()
    print("==============================================================  100 in system  ===============================================================")
    
    todos_setup_populated()
    print("POST request:")
    test_post_todos()
    print()
    print("PUT request:")
    test_update_todos()
    print()
    print("DELETE request:")
    test_delete_todos() 
        
    print()
    print("==============================================================  500 in system  ===============================================================")
    
    todos_setup_very_populated()
    print("POST request:")
    test_post_todos()
    print()
    print("PUT request:")
    test_update_todos()
    print()
    print("DELETE request:")
    test_delete_todos() 
    