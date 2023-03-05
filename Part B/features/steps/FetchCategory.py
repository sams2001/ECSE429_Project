import requests
from behave import *
import json

url = 'http://localhost:4567/categories'

json_header = {"Content-Type": "application/json"}

category_id = None


@given("existing categories in the system")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    category = {
        "title": "Registration",
        "description": "relating to registering for courses"
    }

    category2 = {
        "title": "Project Planning",
        "description": "relating to planning and logistics of projects"
    }

    request1 = requests.post(url, data=json.dumps(category), headers=json_header)
    request2 = requests.post(url, data=json.dumps(category2), headers=json_header)

    global category_id
    category_id = request1.json()["id"]
    assert(request1.status_code == 201)
    assert(request2.status_code == 201)


@when("a user fetches a category by providing the category id")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    r = requests.get(url + f"/{category_id}")
    context.request = r.json()
    assert r.status_code == 200


@then("the system will return the category and its corresponding id, {description}, and {title}")
def step_impl(context, description, title):
    """
    :type context: behave.runner.Context
    :type description: str
    :type title: str
    """

    category = context.request["categories"][0]
    assert category["description"] == description and category["title"] == title


@when("a user fetches all categories")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    r = requests.get(url)
    context.request = r.json()
    assert r.status_code == 200


@then("all categories in the system will be returned")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    categories = context.request["categories"]

    assert len(categories) > 1


@given("there are no categories with {incorrectId} in the system")
def step_impl(context, incorrectId):
    """
    :type context: behave.runner.Context
    :type incorrectId: str
    """
    r = requests.get(url + f"/{incorrectId}")
    assert r.status_code == 404


@when("a user elects to fetch a category by providing the {incorrectId}")
def step_impl(context, incorrectId):
    """
    :type context: behave.runner.Context
    :type incorrectId: str
    """
    r = requests.get(url + f"/{incorrectId}")
    context.error_request = r.json()


@then("an error message is returned containing the {incorrectId}")
def step_impl(context, incorrectId):
    """
    :type context: behave.runner.Context
    :type incorrectId: str
    """
    assert context.error_request["errorMessages"] is not None
