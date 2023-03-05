import requests
from behave import *
import json

url = 'http://localhost:4567/projects'

json_header = {"Content-Type": "application/json"}


@when("a user creates a new project with a {title}, {description}, {completed} status, and {active} status")
def step_impl(context, title, description, completed, active):
    """
    :type context: behave.runner.Context
    :type title: str
    :type description: str
    :type completed: str
    :type active: str
    """
    project_json = {
        "title": title,
        "description": description,
        "completed": json.loads(completed.lower()),
        "active": json.loads(active.lower())
    }

    request = requests.post(url, data=json.dumps(project_json), headers=json_header)
    assert (request.status_code == 201)


@then(
    "a new project is created with {title}, {description}, {completed} status, {active} status, and an auto-generated "
    "id")
def step_impl(context, title, description, completed, active):
    """
    :type context: behave.runner.Context
    :type title: str
    :type description: str
    :type completed: str
    :type active: str
    """

    r = requests.get(url)
    projects = r.json()["projects"]
    created = False

    for project in projects:
        if project["title"] == title and project["description"] == description and project["completed"] == \
                completed.lower() and project["active"] == active.lower():
            created = True

    assert (r.status_code == 200 and created)


@when("a user attempts to create a new project by providing an {unnecessaryId} in the call statement")
def step_impl(context, unnecessaryId):
    """
    :type context: behave.runner.Context
    :type unnecessaryId: str
    """
    request = requests.post(url + f"/{unnecessaryId}")
    context.error_request = request.json()
    assert (request.status_code == 404)


@then(
    'no new project will be created, and an error with the error message "No such project entity instance with GUID '
    'or ID {unnecessaryId} found" will be returned')
def step_impl(context, unnecessaryId):
    """
    :type context: behave.runner.Context
    :type unnecessaryId: str
    """
    assert f"No such project entity instance with GUID or ID {unnecessaryId} found" in \
           context.error_request["errorMessages"]


@when("a user creates a new project without entering information into any of the fields")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    project_json = {}

    request = requests.post(url, data=json.dumps(project_json), headers=json_header)
    assert request.status_code == 201


@then("a new project is created with an auto-generated id, a false {completed} status, a false {active} status, a blank {title}, and a blank {description}")

def step_impl(context):
    r = requests.get(url)
    projects = r.json()["projects"]
    created = False

    for project in projects:
        if project["title"] == "" and project["description"] == "" and project["completed"] == \
                "false" and project["active"] == "false":
            created = True

    assert (r.status_code == 200 and created)
