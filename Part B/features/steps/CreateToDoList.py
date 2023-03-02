import requests
from behave import *
import json

url = 'http://localhost:4567/todos'

json_header = {"Content-Type": "application/json"}

@given("the project is running")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    return

@when("a user creates a new todo item with {title}, {doneStatus}, {description}")
def step_impl(context, title, doneStatus, description):

    """
    :type context: behave.runner.Context
    :type title: str
    :type description: str
    :type doneStatus: str
    """

    todo_item = {
        "doneStatus": json.loads(doneStatus.lower()),
        "title": title,
        "description": description
    }

    request = requests.post(url, data=json.dumps(todo_item), headers=json_header)
    assert(request.status_code == 201)

@when("a user attempts to create a new todo item with {title}, {doneStatus}, {description}, {id}")
def step_impl(context, title, doneStatus, description, id):

    """
    :type context: behave.runner.Context
    :type title: str
    :type description: str
    :type doneStatus: str
    :type id: str
    """

    todo_item = {
        "doneStatus": json.loads(doneStatus.lower()),
        "title": title,
        "description": description,
        "id": int(id)
    }

    request = requests.post(url, data=json.dumps(todo_item), headers=json_header)
    assert(request.status_code == 400)

@then("a new todo item is created with {title}, {doneStatus}, {description}")
def step_impl(context, title, doneStatus, description):
    """
    :type context: behave.runner.Context
    :type title: str
    :type description: str
    :type doneStatus: str
    """
    r = requests.get(url)
    todos = r.json()["todos"]
    created = False

    for todo in todos:
        if todo["title"] == title and todo["description"] == description and todo["doneStatus"] == doneStatus.lower():
            created = True
            
    assert(r.status_code == 200 and created)

@then("no new item is created")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    return



