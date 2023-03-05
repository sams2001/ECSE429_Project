import requests
from behave import *
import json

url= 'http://localhost:4567/'
json_header = {"Content-Type": "application/json"}
errorstack = []

@when(u'a user fetches projects via task id {taskid}')
def step_impl(context,taskid):
    """
    :type context: behave.runner.Context
    :type taskid: str
    """
    #GET /todos/:id/tasksof
    response = requests.get(url+'todos/'+taskid+'/tasksof')
    if 'errorMessage' in str(response.json()):
        errorstack.push(str(response.json()))
    try:
        assert response.status_code==200
    except:
        assert response.status_code==404


@then(u'the project {projectid} related to task {taskid} shall be returned')
def step_impl(context, projectid, taskid):
    """
    :type context: behave.runner.Context
    :type projectid: str
    :type taskid: str
    """
    response = requests.get(url+'todos/'+taskid+'/tasksof')
    assert response.status_code == 200
    projInList = False
    for proj in response.json()['projects']:
        if projectid in str(proj['id']):
            projInList = True
    assert projInList == True



@given(u'todo with id {taskid} exists in the system with no related projects')
def step_impl(context,taskid):
    """
    :type context: behave.runner.Context
    :type projectid: str
    :type taskid: str
    """
    """
    :type context: behave.runner.Context
    :type id: str
    """
    response = requests.get(url+'todos/'+taskid)
    if response.status_code != 200:
        newid=0
        while response.status_code != 200 and newid < int(taskid):
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
            response = requests.get(url+'/todos'+taskid)
    response = requests.get(url+'todos/'+taskid)
    assert response.status_code == 200
    try:
        response = requests.get(url+'todos/'+taskid+'/tasksof')
        assert len(response.json()['projects']) == 0
    except:
        response = requests.get(url+'todos/'+taskid+'/tasksof')
        for proj in response.json()['projects']:
            del_response = requests.delete(url+'todos/'+taskid+'/tasksof/'+str(proj['id']))
            assert del_response.status_code==200
        response = requests.get(url+'todos/'+taskid+'/tasksof')
        assert len(response.json()['projects']) == 0



@then(u'an empty list of projects related to task {taskid} shall be returned')
def step_impl(context, taskid):
    """
    :type context: behave.runner.Context
    :type taskid: str
    """
    response = requests.get(url+'todos/'+taskid+'/tasksof')
    assert response.status_code == 200
    assert len(response.json()['projects']) == 0


@given(u'todo with id {taskid} does not exist')
def step_impl(context,taskid):
    """
    :type context: behave.runner.Context
    :type taskid: str
    """   
    response = requests.get(url+'todos/'+taskid)
    if response.status_code==200:
        del_response = requests.delete(url+'todos/'+taskid)
        response = requests.get(url+'todos/'+taskid)
    assert response.status_code==404
    

@then(u'an error message shall be returned')
def step_impl(context):
    try:
        if 'errorMessage' in errorstack.pop():
            assert True
    except:
        print("ERROR: Fetch project by task will return any existing project even if task does not exist")
        assert False
    