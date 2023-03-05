import requests
from behave import *
import json

todo_url = 'http://localhost:4567/todos'

category_url = 'http://localhost:4567/categories'

json_header = {"Content-Type": "application/json"}

todo_id1 = None
todo_id2 = None


@given(
    "a todo with {title}, {description}, {doneStatus} and at least one category exist in the system with an existing "
    "relationship to category with id {categoryId}")
def step_impl(context, title, description, doneStatus, categoryId):
    """
    :type context: behave.runner.Context
    :type title: str
    :type description: str
    :type doneStatus: str
    :type categoryId: str
    """

    todo_item1 = {
        "doneStatus": json.loads(doneStatus.lower()),
        "title": title,
        "description": description
    }

    request = requests.post(todo_url, data=json.dumps(todo_item1), headers=json_header)
    global todo_id1
    todo_id1 = request.json()["id"]
    assert (request.status_code == 201)

    response = requests.post("http://localhost:4567/todos/" + todo_id1 + '/categories',
                             data=json.dumps({"id": categoryId}), headers=json_header)
    assert response.status_code == 201

    response = requests.post("http://localhost:4567/categories/" + categoryId + '/todos',
                             data=json.dumps({"id": todo_id1}), headers=json_header)
    assert response.status_code == 201


@when("a user fetches the todo items of a category by providing the category id {categoryId}")
def step_impl(context, categoryId):
    """
    :type context: behave.runner.Context
    :type categoryId: str
    """
    request = requests.get(category_url + f"/{categoryId}/todos")
    assert request.status_code == 200
    context.request = request.json()


@then(
    "the system will return all todos relating to the category, as well as the corresponding id, {description}, "
    "{title}, {doneStatus}, {taskOf}, and {categoryId} associated with the todos")
def step_impl(context, description, title, doneStatus, taskOf, categoryId):
    """
    :type context: behave.runner.Context
    :type description: str
    :type title: str
    :type doneStatus: str
    :type taskOf: str
    :type categoryId: str
    """
    todo = context.request["todos"][0]
    assert todo["description"] == description and todo["title"] == title \
           and todo["doneStatus"] == doneStatus.lower().strip() and todo["categories"][0]["id"] == categoryId


@when("a user fetches the todos of a category without specifying the category id")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    request = requests.get(category_url + "/:id/todos")
    assert request.status_code == 200
    context.error_request_unspecified_id = request.json()


@then(
    "the system will return all todos in the system that have relationships with any category and their corresponding "
    "id, {description}, {title}, {doneStatus}, {taskOf}, and {categoryId} associated with the todos")
def step_impl(context, description, title, doneStatus, taskOf, categoryId):
    """
    :type context: behave.runner.Context
    :type description: str
    :type title: str
    :type doneStatus: str
    :type taskOf: str
    :type categoryId: str
    """
    expected_response = requests.get(category_url + f"/{categoryId}/todos")
    assert expected_response.json() != context.error_request_unspecified_id


@when("a user elects to fetch all todos related to a category by providing the category {incorrectId}")
def step_impl(context, incorrectId):
    """
    :type context: behave.runner.Context
    :type incorrectId: str
    """
    request = requests.get(category_url + f"/{incorrectId}/todos")
    assert request.status_code == 200
    context.error_request_unspecified_id = request.json()
