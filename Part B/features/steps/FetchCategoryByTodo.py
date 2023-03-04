import requests
from behave import *
import json

url= 'http://localhost:4567/'
json_header = {"Content-Type": "application/json"}


@then(u'fetching categories via todo {todoid} will return the category {categoryid} associated with todo {todoid}')
def step_impl(context,todoid,categoryid):
    """
    :type context: behave.runner.Context
    :type todoid: str
    :type categoryid: str
    """
    response = requests.get(url+'todos/'+todoid+'/categories')
    assert response.status_code==200
    response_categories = response.json()['categories']
    assert categoryid in str(response_categories)


@given(u'that todo with id {todoid} has a relationship to the categories with ids {categoryids}')
def step_impl(context,todoid,categoryids):
    """
    :type context: behave.runner.Context
    :type todoid: str
    :type categoryids: str
    """
    response = requests.get(url+'todos/'+todoid+'/categories')
    assert response.status_code==200
    categoryidlst = categoryids.strip().split(',')
    for categoryid in categoryidlst:
        try:
            assert categoryid in response.json()['categories'][0]
        except AssertionError:
            json_data = {
                "id": categoryid
            }
            response = requests.post(url+'todos/'+todoid+'/categories', data=json.dumps(json_data), headers=json_header)
            assert response.status_code == 201
            response = requests.get(url+'todos/'+todoid+'/categories')
            assert response.status_code == 200
            assert categoryid in str(response.json()['categories'])


@then(u'fetching categories via todo {todoid} will return all of the categories {categoryids} associated with todo {todoid}')
def step_impl(context,todoid,categoryids):
    """
    :type context: behave.runner.Context
    :type todoid: str
    :type categoryids: str
    """
    categoryidlst = categoryids.strip().split(',')
    response = requests.get(url+'todos/'+todoid+'/categories')
    assert response.status_code==200
    response_categories = response.json()['categories']
    for categoryid in categoryidlst:
        assert categoryid in str(response_categories)


@given(u'that categories with ids {categoryids} exists in the system')
def step_impl(context,categoryids):
    """
    :type context: behave.runner.Context
    :type categoryids: str
    """
    categoryidlst = categoryids.strip().split(',')
    for categoryid in categoryidlst:
        response = requests.get(url+'categories/'+categoryid)
        if response.status_code == 404:
            json_1 = {
                "title": "Work",
                "description": ""
            }
            response1 = requests.post(url+'categories',data=json.dumps(json_1),headers=json_header)
            assert response1.status_code == 201 
            response = requests.get(url+'/'+categoryid)
        assert response.status_code == 200


@then(u'fetching categories via todo {todoid} will return an error message')
def step_impl(context,todoid):
    """
    :type context: behave.runner.Context
    :type todoid: str
    """
    response = requests.get(url+'todos/'+todoid+'/categories')
    try:
        assert response.status_code==400
    except:
        assert response.status_code==404
    finally:
        print('ERROR: service fails, fetching categories via a todo that does not exist returns categories')
