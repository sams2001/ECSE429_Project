import requests
from behave import *
import json

url = 'http://localhost:4567/projects'

json_header = {"Content-Type": "application/json"}

test_id = 0


@given("project(s) exist in the system with a {title}, {description}, {completed} status, and {active} status")
def step_impl(context, title, description, completed, active):
    """
    :type context: behave.runner.Context
    :type title: str
    :type description: str
    :type completed: str
    :type active: str
    """

    project = {
        "title": title,
        "description": description,
        "completed": json.loads(completed.lower()),
        "active": json.loads(active.lower())
    }

    request = requests.post(url, data=json.dumps(project), headers=json_header)
    global test_id
    test_id = request.json()["id"]

    assert (request.status_code == 201)


@given("there is no existent project with {incorrectId} in the system")
def step_impl(context, incorrectId):
    """
    :type context: behave.runner.Context
    :type incorrectId: str
    """

    request = requests.get(url + incorrectId)
    assert (request.status_code == 404)


@when("a user elects to delete a project by correctly providing the project id")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    request = requests.delete(url + "/" + str(test_id))
    assert (request.status_code == 200)


@when("a user elects to delete a project by providing the {incorrectId}")
def step_impl(context, incorrectId):
    """
    :type context: behave.runner.Context
    :type incorrectId: str
    """

    request = requests.delete(url + "/" + incorrectId)
    context.error_request = request.json()
    assert (request.status_code == 404)


@then("the project with the provided id will be removed from the system")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    request = requests.get(url + "/" + str(test_id))
    assert (request.status_code == 404)


@then('no project will be removed from the system, and an error message is returned')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.error_request["errorMessages"] is not None


@when("a user elects to delete a project, but does not specify a project id")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    request = requests.delete(url+"/:id")
    context.error_request = request


@then('no project will be removed from the system, a "404 Not Found" Error occurs, and the return statement is blank')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert 'Could not find any instances with projects/:id' in context.error_request.json()["errorMessages"]
    assert context.error_request.status_code == 404
