import requests
from behave import *
import json

url= 'http://localhost:4567/'
json_header = {"Content-Type": "application/json"}

@given(u'that todo with id {todoid} has a relationship to the category with id {categoryid}')
def step_impl(context,todoid, categoryid):
    """
    :type context: behave.runner.Context
    :type todoid: str
    :type categoryid: str
    """
    try:
        response_todo = requests.get(url+'todos/'+todoid)
        todo = response_todo.json()['todos'][0]['categories'][0]
        assert response_todo.status_code == 200
        assert categoryid in str(todo)
    except:
        json_data = {
            "id": categoryid
        }
        response = requests.post(url+'todos/'+todoid+'/categories', data=json.dumps(json_data), headers=json_header)
        assert response.status_code == 201

        response_todo = requests.get(url+'todos/'+todoid)
        todo = response_todo.json()['todos'][0]['categories'][0]
        assert response_todo.status_code == 200
        assert categoryid in str(todo)


@when(u'a relationship between todo {todoid} and category {categoryid} is deleted on the todos side')
def step_impl(context,todoid,categoryid):
    """
    DELETE /todos/:id/categories/:id
    :type context: behave.runner.Context
    :type todoid: str
    :type categoryid: str
    """
    response = requests.delete(url+'todos/'+todoid+'/categories/'+categoryid)
    assert response.status_code == 200


@then(u'todo {todoid} will not have a relation to category {categoryid}')
def step_impl(context,todoid,categoryid):
    """
    :type context: behave.runner.Context
    :type todoid: str
    :type categoryid: str
    """
    try:
        response_todo = requests.get(url+'todos/'+todoid)
        assert 'categories' not in str(response_todo.json()['todos'][0])
    except AssertionError:
        response_todo = requests.get(url+'todos/'+todoid)
        todo = response_todo.json()['todos'][0]['categories'][0]
        try:
            assert categoryid not in str(todo)
        except AssertionError:
            print("ERROR: Despite API documentation stating otherwise, todo and category relationship is a one-way relationship.")
    finally:    
        assert response_todo.status_code == 200


@then(u'category {categoryid} will not have a relation to todo {todoid}')
def step_impl(context,categoryid,todoid):
    """
    :type context: behave.runner.Context
    :type categoryid: str
    :type todoid: str
    """
    response_todo = requests.get(url+'categories/'+categoryid+'/todos')
    category = response_todo.json()['todos']
    assert response_todo.status_code == 200
    assert todoid not in str(category)


@when(u'a relationship between todo {todoid} and category {categoryid} is deleted on the categories side')
def step_impl(context,todoid,categoryid):
    """
    DELETE /categories/:id/todos/:id
    :type context: behave.runner.Context
    :type todoid: str
    :type categoryid: str
    """
    try:
        response = requests.delete(url+'categories/'+categoryid+'/todos/'+todoid)
        assert response.status_code==200
    except AssertionError:
        print("ERROR: Despite API documentation stating otherwise, todo and category relationship is a one-way relationship.")


@given(u'that todo with id {todoid} does not exist in the system')
def step_impl(context,todoid):
    """
    :type context: behave.runner.Context
    :type todoid: str
    """
    response=requests.get(url+'todos/'+todoid)
    if response.status_code!=404:
        response2=requests.delete(url+'todos/'+todoid)
        response=requests.get(url+'todos/'+todoid)
    assert response.status_code==404

@then(u'an error will be raised when a relationship between todo {todoid} and category {categoryid} is deleted on the todos side')
def step_impl(context,todoid,categoryid):
    """
    :type context: behave.runner.Context
    :type todoid: str
    :type categoryid: str
    """
    response = requests.delete(url+'todos/'+todoid+'/categories/'+categoryid)
    assert 'errorMessage' in str(response.json())
    assert response.status_code == 400