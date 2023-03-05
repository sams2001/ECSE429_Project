import requests
from behave import *
import json

url = 'http://localhost:4567/'

json_header = {"Content-Type": "application/json"}

@given(u'todos with ids {todoids} exist in the system')
def step_impl(context,todoids):
    """
    :type context: behave.runner.Context
    :type todoids: str
    """
    todoidlst = todoids.strip().split(',')
    for id in todoidlst:
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


@given(u'a project with id {projectid} exists with related tasks {taskids}')
def step_impl(context,projectid,taskids):
    """
    :type context: behave.runner.Context
    :type projectid: str
    :type taskids: str
    """
    taskidlst = taskids.strip().split(",")

    response = requests.get(url+'projects/'+projectid)
    if response.status_code == 200:
        for taskid in taskidlst:
            try:
                response = requests.get(url+'projects/'+projectid+'/tasks')
                assert taskid in str(response.json())
            except AssertionError:
                post = requests.post(url+'projects/'+projectid+'/tasks', data=json.dumps({"id":taskid}), headers=json_header)
                assert post.status_code == 201
                response = requests.get(url+'projects/'+projectid+'/tasks')
                assert taskid in str(response.json())

    elif response.status_code == 404:
        project_payload = {
            "title": "Work",
            "completed": False,
            "active": False,
            "description": "",
            "tasks": []
            }
        post1 = requests.post(url+'projects', data=json.dumps(project_payload), headers=json_header)
        assert post1.status_code == 201
        #POST /projects/:id/tasks
        for taskid in taskidlst:
            post2 = requests.post(url+'projects/'+projectid+'/tasks', data=json.dumps({"id":taskid}), headers=json_header)
            assert post2.status_code == 201
    else:
        assert False


@when(u'a user fetches tasks via project with project id {projectid}')
def step_impl(context,projectid):
    """
    :type context: behave.runner.Context
    :type projectid: str
    """
    response = requests.get(url+'projects/'+projectid+'/tasks')
    #found or not found, no other status codes
    try:
        assert response.status_code == 200
    except:
        assert response.status_code == 404


@then(u'the tasks {taskids} related to project {projectid} shall be returned')
def step_impl(context,taskids,projectid):
    """
    :type context: behave.runner.Context
    :type taskids: str
    :type projectid: str
    """
    taskidlst = taskids.strip().split(',')
    response = requests.get(url+'projects/'+projectid+'/tasks')
    for taskid in taskidlst:
        assert taskid in str(response.json())


@given(u'a project with id {projectid} exists with no related tasks')
def step_impl(context,projectid):
    """
    :type context: behave.runner.Context
    :type projectid: str
    """
    response = requests.get(url+'projects/' + projectid)
    if response.status_code == 200:
        try:
            assert 'tasks' not in str(response.json()['projects'][0])
        except:
            #DELETE /projects/:id/tasks/:id
            tasks = response.json()['projects'][0][tasks]
    else:
        newid = 0
        while response.status_code != 200 and newid<int(projectid):
            project_payload = {
                "title": "Work",
                "completed": False,
                "active": False,
                "description": "",
                "tasks": []
            }
            response1 = requests.post(url+'projects',data=json.dumps(project_payload),headers=json_header)
            print(str(response1.json()))
            newid = int(response1.json()['id'])
            assert response1.status_code == 201 
            response = requests.get(url+'projects/' + projectid)
        print(str(response.json()))
        assert 'tasks' not in str(response.json()['projects'][0])



@then(u'no tasks related to project {projectid} shall be returned')
def step_impl(context,projectid):
    """
    :type context: behave.runner.Context
    :type projectid: str
    """
    response = requests.get(url+'projects/'+projectid)
    try:
        assert 'tasks' not in str(response.json()['projects'][0])
    except:
        assert len(response.json()['projects'][0]['tasks']) == 0