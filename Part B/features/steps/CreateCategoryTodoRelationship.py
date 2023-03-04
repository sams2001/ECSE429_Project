import requests
from behave import *
import json

url = 'http://localhost:4567/'
json_header = {"Content-Type": "application/json"}

@given(u'that category with id {id} exists in the system')
def step_impl(context,id):
    """
    :type context: behave.runner.Context
    :type id: str
    """
    response = requests.get(url+'categories/'+id)
    if response.status_code == 404:
        json_1 = {
            "title": "Work",
            "description": ""
        }
        response1 = requests.post(url+'categories',data=json.dumps(json_1),headers=json_header)
        assert response1.status_code == 201 
        response = requests.get(url+'/categories/'+id)
    assert response.status_code == 200
    

@given(u'that todo with id {id} exists in the system')
def step_impl(context,id):
    """
    :type context: behave.runner.Context
    :type id: str
    """
    response = requests.get(url+'todos/'+id)
    if response.status_code != 200:
        newid=0
        while response.status_code != 200 and newid < int(id):
            json_2 = {
                "title": "delete paperwork",
                "doneStatus": False,
                "description": "",
                "tasksof": [
                    {
                    "id": "1"
                    }
                ]
            }
            response1 = requests.post(url+'todos',data=json.dumps(json_2),headers=json_header)
            newid = int(response1.json()['id'])
            assert response1.status_code == 201 
            response = requests.get(url+'/'+id)
    response = requests.get(url+'todos/'+id)
    assert response.status_code == 200


@given(u'that todo with id {todoid} has no relationship to the category with {categoryid}')
def step_impl(context, todoid,categoryid):
    """
    :type context: behave.runner.Context
    :type todoid: str
    :type categoryid: str
    """
    response = requests.get(url+'todos/'+todoid)
    if 'categories' in response.json()["todos"][0]:
        assert categoryid not in response.json()["todos"][0]['categories']
    else:
        assert 'categories' not in response.json()["todos"][0]


@when(u'a relationship between todo {todoid} and category {categoryid} is instantiated')
def step_impl(context,todoid,categoryid):
    """
    :type context: behave.runner.Context
    :type todoid: str
    :type categoryid: str
    """
    json_3 = {
        "id": categoryid
    }
    response = requests.post(url+'todos/'+todoid+'/categories', data=json.dumps(json_3), headers=json_header)
    assert response.status_code == 201


@then(u'todo {todoid} will have a relation to category {categoryid}')
def step_impl(context,todoid,categoryid):
    """
    :type context: behave.runner.Context
    :type todoid: str
    :type categoryid: str
    """
    try:
        response = requests.get(url+'todos/'+todoid).json()['todos'][0]['categories'][0]
        assert categoryid in str(response)
        
        response = requests.get(url+'categories/'+categoryid+'/todos').json()['todos']
        assert todoid in str(response)
    except AssertionError:
        print("ERROR: Despite API documentation stating otherwise, todo and category relationship is a one-way relationship.")
        assert False

@when(u'a new todo is created with a relationship to category {categoryid}')
def step_impl(context,categoryid):
    """
    :type context: behave.runner.Context
    :type categoryid: str
    """
    json_4 = {
        "title": "delete paperwork",
        "doneStatus": False,
        "description": "",
        "tasksof": [
            {
            "id": "1"
            }
        ],
        "categories": [
            {
            "id": categoryid
            }
        ]
    }
    response = requests.post(url+'todos', data=json.dumps(json_4), headers=json_header)
    try:
        assert response.status_code == 400 
    except AssertionError:
        assert response.status_code == 201 #depends on story, but should be one or other



@then(u'the new todo will have a relation to category {categoryid}')
def step_impl(context,categoryid):
    """
    :type context: behave.runner.Context
    :type categoryid: str
    """
    #last element of get all todos will be the new one
    todoslst = requests.get(url+'todos').json()["todos"]
    newtodo = [todo for todo in todoslst if int(todo['id']) == len(todoslst)]
    assert categoryid == newtodo[0]['categories'][0]['id']

@given(u'that category with id {categoryid} does not exist in the system')
def step_impl(context,categoryid):
    """
    :type context: behave.runner.Context
    :type categoryid: str
    """
    response = requests.get(url+'categories/'+categoryid)
    if response.status_code != 404:
        response2 = requests.delete(url+'categories/'+categoryid)
        response = requests.get(url+'categories/'+categoryid)
    assert response.status_code == 404

@then(u'the new todo will not have a relation to category {categoryid}')
def step_impl(context,categoryid):
    """
    :type context: behave.runner.Context
    :type categoryid: str
    """   
    todoslst = requests.get(url+'todos').json()["todos"]
    newtodo = todoslst[len(todoslst)-1]
    try:
        assert categoryid not in newtodo['categories']
    except AssertionError:
        assert 'categories' not in str(newtodo)
