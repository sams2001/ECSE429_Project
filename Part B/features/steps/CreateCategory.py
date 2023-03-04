import requests
from behave import *
import json

url = 'http://localhost:4567/categories'

json_header = {"Content-Type": "application/json"}


@when(u'a user creates a new category with a {title} and {description}')
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
    assert(request.status_code == 201)


@when("a user creates a new category by providing a valid {title}, and leaves the description blank")
def step_impl(context, title):
    """
    :type context: behave.runner.Context
    :type title: str
    """

    category = {
        "title": title, 
    }

    request = requests.post(url, data=json.dumps(category), headers=json_header)
    assert(request.status_code == 201)


@when("a user attempts to create a new category but provides a {blankTitle}, and a valid {description}")
def step_impl(context, blankTitle, description):
    """
    :type context: behave.runner.Context
    :type blankTitle: str
    :type description: str
    """

    category = {
        "description": description
    }

    request = requests.post(url, data=json.dumps(category), headers=json_header)
    context.error_request = request.json()
    assert(request.status_code == 400)


@then("a new category is created with {title}, {description} and an auto-generated id")
def step_impl(context, title, description):
    """
    :type context: behave.runner.Context
    :type title: str
    :type description: str

    """
    r = requests.get(url)
    categories = r.json()["categories"]
    created = False

    for category in categories:
        if category["title"] == title:
            created = True

    assert(r.status_code == 200 and created)


@then('no new item is created, and an error message "title : field is mandatory" is returned')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert "title : field is mandatory" in context.error_request["errorMessages"]


