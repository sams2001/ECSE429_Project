import requests
from behave import *
import json
import os

url = 'http://localhost:4567/projects'

json_header = {"Content-Type": "application/json"}

@given(u'a project with id {id} exists')
def step_impl(context, id):
    """
    :type context: behave.runner.Context
    :type id: str
    """
    id = id.strip('\"')
    response = requests.get(url+'/'+id)
    if (response.status_code != 200):
        proj_json = {
            "title": "Office Work",
            "completed": "false",
            "active": "false",
            "description": "",
            "tasks": [
                {
                "id": "2"
                },
                {
                "id": "1"
                }
            ]
        }
        response = requests.post(url, data=json.dumps(proj_json), headers=json_header)
        print("posting: " + str(response.json()))
        assert response.status_code == 201
        response = requests.get(url+'/'+id)
    response = requests.get(url+'/'+id)
    assert response.status_code == 200
    assert id == response.json()["projects"][0]['id']


@when(u'a user initiates the update of the project with id {id} to title {title}, completed status {completedStatus}, active status {activeStatus}, and description {description}')
def step_impl(context, id, title, completedStatus, activeStatus, description):
    """
    :type context: behave.runner.Context
    :type id: str
    :type title: str
    :type completedStatus: str
    :type activeStatus: str
    :type description: str
    """

    if 'true' in completedStatus:
        completedStatus=True
    else:
        completedStatus=False

    if 'true' in activeStatus:
        activeStatus=True
    else:
        activeStatus=False

    id = id.strip('\"')
    
    proj_json = {
            "title": title,
            "completed": completedStatus,
            "active": activeStatus,
            "description": description,
            "tasks": []
        }
    response = requests.put(url+'/'+id, data=json.dumps(proj_json), headers=json_header)
    print("after put: 1 " + str(response.json()))


@then(u'the project with id {id} will have title {title}, completed status {completedStatus}, active status {activeStatus}, and description {description}')
def step_impl(context,id,title,completedStatus,activeStatus,description):
    """
    :type context: behave.runner.Context
    :type id: str
    :type title: str
    :type completedStatus: str
    :type activeStatus: str
    :type description: str
    """
    response = requests.get(url+'/'+id.strip('\"'))
    assert response.status_code == 200
    assert title == response.json()["projects"][0]['title']
    assert description == response.json()["projects"][0]['description']


@when(u'a user initiates the update of the project with id {id} to title {title}, completed status {completedStatus}, active status {activeStatus}, description {description}, and tasks {tasks}')
def step_impl(context,id,title,completedStatus,activeStatus,description,tasks):
    """
    :type context: behave.runner.Context
    :type id: str
    :type title: str
    :type completedStatus: str
    :type activeStatus: str
    :type description: str
    :type tasks: str
    """
    if tasks=="":
        tasklst = ""
    else:
        tasks.strip()
        tasks.strip('\"')
        tasklst = tasks.split(',')
    if 'true' in completedStatus:
        completedStatus=True
    else:
        completedStatus=False

    if 'true' in activeStatus:
        activeStatus=True
    else:
        activeStatus=False

    proj_json = {
        "title": title,
        "completed": completedStatus,
        "active": activeStatus,
        "description": description,
        "tasks": [tasklst]
    }
    id=id.strip('\"') 
    response=requests.put(url+'/'+id, data=json.dumps(proj_json), headers=json_header)
    print("after put:  " + str(response.json()))


@then(u'the project with id {id} will have title {title}, completed status {completedStatus}, active status {activeStatus}, description {description}, and tasks {tasks}')
def step_impl(context,id,title,completedStatus,activeStatus,description,tasks):
    """
    :type context: behave.runner.Context
    :type id: str
    :type title: str
    :type completedStatus: str
    :type activeStatus: str
    :type description: str
    :type tasks: str
    """
    tasklst = tasks.strip().strip('\"').split(',')
    id = id.strip('\"')
    response = requests.get(url+'/'+id)
    assert response.status_code == 200
    print(response.json())
    print(title, completedStatus, activeStatus)
    assert title.strip('\"') == response.json()["projects"][0]['title']
    assert description.strip('\"') == response.json()["projects"][0]['description']
    assert len(tasklst) == len(response.json()["projects"][0]['tasks'])


@then(u'the project with id {id} will not exist')
def step_impl(context, id):
    """
    :type context: behave.runner.Context
    :type id: str
    """

    response = requests.get(url+'/'+id.strip('\"'))
    assert response.status_code == 404


@given(u'a project with id {id} does not exist')
def step_impl(context,id):
    """
    :type context: behave.runner.Context
    :type id: str
    """    
    id=id.strip('\"')
    response = requests.get(url+'/'+id)
    if response.status_code != 404:
        requests.delete(url+'/'+id)
    response = requests.get(url+'/'+id)
    assert response.status_code == 404