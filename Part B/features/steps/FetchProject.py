import requests
from behave import *
import json

url = 'http://localhost:4567/projects'

json_header = {"Content-Type": "application/json"}

app_project = requests.Response

project_id = 0


@given("a project exists in the system with with a {title}, {description}, {completed} status, and {active} status")
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
    global project_id
    project_id = request.json()["id"]
    response = requests.get(url + '/' + project_id)

    assert response.status_code == 200


@when(u'a user fetches a project by providing the project id')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    global app_project
    app_project = requests.get(url + '/' + str(project_id))
    assert app_project is not None


@then(u'the system will return the project and its corresponding and related fields')
def step_impl(context):
    global app_project
    assert project_id == app_project.json()["projects"][0]['id']
    assert 'title' in app_project.json()["projects"][0]
    assert 'completed' in app_project.json()["projects"][0]
    assert 'active' in app_project.json()["projects"][0]
    assert 'description' in app_project.json()["projects"][0]


@given(u'at least one project exists in the system')
def step_impl(context):
    response = requests.get(url)

    if len(response.json()["projects"]) == 0:
        project_json = {
            "title": "Big Proj 1",
            "description": "relating to registering for courses",
            "completed": json.loads("false"),
            "active": json.loads("true")
        }
        requests.post(url, data=json.dumps(project_json), headers=json_header)
        response = requests.get(url + '/' + id)

    assert len(response.json()["projects"]) >= 1


@when(u'a user fetches project(s) without providing a specific project id')
def step_impl(context):
    global app_project
    app_project = requests.get(url)
    assert app_project.status_code == 200


@then(u'all projects in the system and their corresponding id, and related fields are returned')
def step_impl(context):
    global app_project
    assert len(app_project.json()["projects"]) >= 1
    for proj in app_project.json()["projects"]:
        assert 'id' in proj
        assert 'title' in proj
        assert 'completed' in proj
        assert 'active' in proj
        assert 'description' in proj


@given(u'there are no projects with {incorrectId} in the system')
def step_impl(context, incorrectId):
    """
    :type context: behave.runner.Context
    """

    response = requests.get(url + '/' + incorrectId)
    if response.status_code != 404:
        requests.delete(url + "/" + incorrectId)
        response = requests.get(url + '/' + incorrectId)

    assert response.status_code == 404


@then(u'a 404 Not Found Error occurs, and the return statement is blank')
def step_impl(context):
    global app_project
    assert app_project.status_code == 404


@when("a user fetches a project by providing the project id {incorrectId}")
def step_impl(context, incorrectId):
    """
    :type context: behave.runner.Context
    :type incorrectId: str
    """
    global app_project
    app_project = requests.get(url + '/' + incorrectId)
    assert app_project is not None
