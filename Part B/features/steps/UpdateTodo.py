import requests
from behave import *
import json

url = 'http://localhost:4567/todos'

json_header = {"Content-Type": "application/json"}

todo_id = None


@given("at least one todo exists in the system")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    todo_item = {
        "doneStatus": json.loads("false"),
        "title": "updating todos",
        "description": "making a test for updating todo items"
    }

    request = requests.post(url, data=json.dumps(todo_item), headers=json_header)
    global todo_id
    todo_id = request.json()["id"]
    assert (request.status_code == 201)


@then(
    "the system will append the changed fields and return the todo and its corresponding id, {title}, {description},"
    "{doneStatus}, and {taskOf}")
def step_impl(context, title, description, doneStatus, taskOf):
    """
    :type context: behave.runner.Context
    :type title: str
    :type description: str
    :type doneStatus: str
    :type taskOf: str
    """
    r = requests.get(url + f"/{todo_id}")
    todo = r.json()["todos"][0]

    updated = False
    if todo["title"] == title and todo["description"] == description and todo["doneStatus"] == doneStatus.lower().strip():
        updated = True

    assert (r.status_code == 200 and updated)


@when("a user updates a todo by only providing the todo id and updated {title}")
def step_impl(context, title):
    """
    :type context: behave.runner.Context
    :type title: str
    """
    todo_item = {
        "title": title,
    }

    request = requests.put(url + f"/{todo_id}", data=json.dumps(todo_item), headers=json_header)

    assert (request.status_code == 200)


@then(
    "the system will append the changed {title} and return the todo and its corresponding information, "
    "the description will be set to an empty string, the doneStatus will be set to false, the taskOf relationship "
    "will be voided")
def step_impl(context, title):
    """
    :type context: behave.runner.Context
    :type title: str
    """
    r = requests.get(url + f"/{todo_id}")
    todo = r.json()["todos"][0]
    updated = False

    if todo["title"] == title and todo["description"] == "" and todo["doneStatus"] == "false":
        updated = True

    assert (r.status_code == 200 and updated)


@given("there are no todos with {incorrectId} in the system")
def step_impl(context, incorrectId):
    """
    :type context: behave.runner.Context
    :type incorrectId: str
    """
    r = requests.get(url + f"/{incorrectId}")
    assert r.status_code == 404


@when("a user elects to update a todo by providing the {incorrectId}")
def step_impl(context, incorrectId):
    """
    :type context: behave.runner.Context
    :type incorrectId: str
    """
    request = requests.put(url + f"/{incorrectId}")
    context.error_request = request.json()


@then('an error message is returned')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.error_request["errorMessages"] is not None


@when("a user updates a todo by providing the todo id and updated {title}, {description}, {doneStatus}, and {taskOf}")
def step_impl(context, title, description, doneStatus, taskOf):
    """
    :type context: behave.runner.Context
    :type title: str
    :type description: str
    :type doneStatus: str
    :type taskOf: str
    """

    todo_item = {
        "doneStatus": json.loads(doneStatus.lower()),
        "title": title,
        "description": description,
        "tasksof": [{"id": taskOf}],
    }

    request = requests.put(url + f"/{todo_id}", data=json.dumps(todo_item), headers=json_header)
    assert (request.status_code == 200)
