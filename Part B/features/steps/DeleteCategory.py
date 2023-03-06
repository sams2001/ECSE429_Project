import requests
from behave import *
import json

url = 'http://localhost:4567/categories'

json_header = {"Content-Type": "application/json"}

test_id = 0


@given("a category exists in the system with {title} and {description}")
def step_impl(context, title, description):
    """
    :type context: behave.runner.Context
    :type title: str
    :type description: str
    """

    category = {
        "title": title,
        "description": description
    }

    request = requests.post(url, data=json.dumps(category), headers=json_header)

    global test_id
    test_id = request.json()["id"]

    assert (request.status_code == 201)


@given("there is no existent category with {incorrectId} in the system")
def step_impl(context, incorrectId):
    """
    :type context: behave.runner.Context
    :type incorrectId: str
    """

    request = requests.get(url + incorrectId)
    assert (request.status_code == 404)


@when("a user elects to delete a category by correctly providing the category id")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    request = requests.delete(url + "/" + str(test_id))
    assert (request.status_code == 200)


@when("a user elects to delete a category by providing the {incorrectId}")
def step_impl(context, incorrectId):
    """
    :type context: behave.runner.Context
    :type incorrectId: str
    """

    request = requests.delete(url + "/" + incorrectId)
    context.error_request = request.json()
    assert (request.status_code == 404)


@then("no category will be removed from the system")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """


@then("the category with the provided id will be removed from the system")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    request = requests.get(url + "/" + str(test_id))
    assert (request.status_code == 404)


@then('no category will be removed from the system, and an error message is returned')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.error_request["errorMessages"] is not None


@when("a user elects to delete a category, but does not specify a category id")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    request = requests.delete(url+"/:id")
    context.error_request = request


@then('no category will be removed from the system, a "404 Not Found" Error occurs, and the return statement is blank')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert 'Could not find any instances with categories/:id' in context.error_request.json()["errorMessages"]
    assert context.error_request.status_code == 404
