import requests
from behave import *
import json

url = 'http://localhost:4567/todos'

json_header = {"Content-Type": "application/json"}

todo_id = None


@given("todos exist in the system")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    todo = {
        "title": "Register for course",
        "description": "register for MECH261",
        "doneStatus" : False,
        "tasksof": [
            {
                "id": "1"
            }
        ],
        "categories": [
            {
                "id": "1"
            }
        ]
    }

    todo2 = {
        "title": "Plan project",
        "description": "create project team",
        "doneStatus" : True,
        "tasksof": [
            {
                "id": "1"
            }
        ],
        "categories": [
            {
                "id": "2"
            }
        ]
    }

    request1 = requests.post(url, data=json.dumps(todo), headers=json_header)
    request2 = requests.post(url, data=json.dumps(todo2), headers=json_header)

    global todo_id
    todo_id = request1.json()["id"]
    assert(request1.status_code == 201)
    assert(request2.status_code == 201)


@when("a user fetches a todo by providing the todo id")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    r = requests.get(url + f"/{todo_id}")
    context.request = r.json()
    assert r.status_code == 200


@then("the system will return the todo and its corresponding id, {description}, {title}, {doneStatus}, {taskOf}, "
      "and {categories} associated with the todo")
def step_impl(context, description, title, doneStatus, taskOf, categories):
    """
    :type context: behave.runner.Context
    :type description: str
    :type title: str
    :type doneStatus: str
    :type taskOf: str
    :type categories:str
    """

    todo = context.request["todos"][0]
    assert todo["description"] == description and todo["title"] == title
    assert todo["doneStatus"] == doneStatus.lower().strip() and todo["tasksof"][0]["id"] == taskOf \
           and todo["categories"][0]["id"] == categories


@when("a user fetches a todo without providing the specific id of the todo")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    r = requests.get(url)
    context.request = r.json()
    assert r.status_code == 200


@then(
    "the system will return all todos in the system and their corresponding id, {description}, {title}, {doneStatus}, "
    "{taskOf}, and {categories} associated with the todos")
def step_impl(context, description, title, doneStatus, taskOf, categories):
    """
    :type context: behave.runner.Context
    :type description: str
    :type title: str
    :type doneStatus: str
    :type taskOf: str
    :type categories: str
    """
    todos = context.request["todos"][0]

    assert len(todos) != 0


@when("a user elects to fetch a todos by providing the {incorrectId}")
def step_impl(context, incorrectId):
    """
    :type context: behave.runner.Context
    :type incorrectId: str
    """
    r = requests.get(url + f"/{incorrectId}")
    context.error_request = r.json()
