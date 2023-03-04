import requests
from behave import *
import json
import os
import subprocess


url = 'http://localhost:4567/categories'

json_1 = """{
        "title": "School",
        "description": "testing"
        }"""

json_header = {"Content-Type": "application/json"}

@given(u'the application is running')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
     
    response = requests.get('http://localhost:4567')
    if response.status_code != 200:
        subprocess.call(['java', '-jar', 'runTodoManagerRestAPI-1.5.5.jar'])
    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'text/html'


@given(u'a category with id \'1\' exists')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
     
    response = requests.get(url+'/1')
    assert response.status_code == 200
    assert 'categories' in response.json()


@when(u'a user initiates the update of the category with id \'1\' to title {title} and description {description}')
def step_impl(context, title, description):
    """
    :type context: behave.runner.Context
    :type title: str
    :type description: str
    """
    category_json = {
        "title": title,
        "description": description    
    }

    response = requests.put(url+'/1', data=json.dumps(category_json), headers=json_header)
    assert(response.status_code == 200)

@then(u'the category with id \'1\' will have title {title} and description {description}')
def step_impl(context, title, description):
    """
    :type context: behave.runner.Context
    :type title: str
    :type description: str
    """
    response = requests.get(url+'/1')
    assert title == response.json()["categories"][0]['title']
    assert description == response.json()["categories"][0]['description']


@given(u'a category with id \'10000\' does not exist')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
     
    response = requests.get(url+'/10000')
    if (response.status_code != 404):
        response = requests.delete(url+'/10000')
        assert response.status_code == 200
    assert response.status_code == 404


@when(u'a user initiates the update of the category with id \'10000\' to title {title} and description {description}')
def step_impl(context, title, description):
    """
    :type context: behave.runner.Context
    :type title: str
    :type description: str
    """

    category_json = {
        "title": title,
        "description": description    
    }

    response = requests.put(url+'/10000', data=json.dumps(category_json), headers=json_header)
    assert response.status_code == 404
    assert 'errorMessages' in response.json()


@then(u'the category with id \'10000\' will not exist')
def step_impl(context):
    response = requests.get(url+'/10000')
    assert response.status_code == 404
    assert 'errorMessages' in response.json()


def after_all(context):
    """
    :type context: behave.runner.Context
    """
    os.system("npx kill-port 4567")
    response = requests.get('http://localhost:4567')
    assert response.status_code == 404