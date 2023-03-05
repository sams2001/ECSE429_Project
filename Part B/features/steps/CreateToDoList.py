import requests
from behave import *
import json

url = 'http://localhost:4567/todos'

json_header = {"Content-Type": "application/json"}

todo_id = None


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
    global todo_id
    todo_id = request.json()["id"]
    assert (request.status_code == 201)


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
    assert (request.status_code == 400)


@then("a new todo item is created with {title}, {doneStatus}, {description}, and an auto-generated id")
def step_impl(context, title, doneStatus, description):
    """
    :type context: behave.runner.Context
    :type title: str
    :type description: str
    :type doneStatus: str
    """
    r = requests.get(url + f"/{todo_id}")
    todo = r.json()["todos"][0]
    created = False

    if todo["title"] == title and todo["description"] == description and todo["doneStatus"] == doneStatus.lower():
        created = True

    assert (r.status_code == 200 and created)


@then("a new todo is created with {title}, a null description, a false done status, and an auto-generated id")
def step_impl(context, title):
    """
        :type context: behave.runner.Context
        :type title: str
    """
    r = requests.get(url)
    todos = r.json()["todos"]
    created = False

    for todo in todos:
        if todo["title"] == title and todo["description"] == "" and todo["doneStatus"] == "false":
            created = True

    assert (r.status_code == 200 and created)

@then("no new item is created")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    return


@when("a user creates a new todo by providing a valid {title}, and leaves the description and done status blank")
def step_impl(context, title):
    """
    :type context: behave.runner.Context
    :type title: str
    """
    todo_item = {
        "title": title,
    }

    request = requests.post(url, data=json.dumps(todo_item), headers=json_header)
    assert (request.status_code == 201)

