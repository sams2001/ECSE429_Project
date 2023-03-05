import requests
from behave import *
import json

url = 'http://localhost:4567/'

json_header = {"Content-Type": "application/json"}



@given(u'todo with id {todoids} exists in the system with no relationship to project {projectid}')
def step_impl(context,todoids,projectid):
    """
    :type context: behave.runner.Context
    :type todoids: str
    :type projectid: str
    """
    todoidlst = todoids.strip().split(',')
    for todoid in todoidlst:
        response = requests.get(url+'todos/'+todoid)
        try:
            assert response.status_code == 200
        except:
            newid=0
            while response.status_code != 200 and newid < int(todoid):
                json_todo = {
                        "title": "delete paperwork",
                        "doneStatus": False,
                        "description": "",
                        "tasksof": []
                    }
                new_proj = requests.post(url+'todos',data=json.dumps(json_todo),headers=json_header)
                newid = int(new_proj.json()['id'])
                assert new_proj.status_code == 201 
                response = requests.get(url+'todos/'+todoid)
            assert response.status_code == 200
        finally:
            try:
                response = requests.get(url+'todos/'+todoid+'/tasksof')
                assert projectid not in str(response.json()['projects'])
            except AssertionError:
                #DELETE /projects/:id/tasks/:id
                response_delete = requests.delete(url+'todos/'+todoid+'/tasksof/'+projectid)
                response = requests.get(url+'todos/'+todoid+'/tasksof')
                for project in response.json()['projects']:
                    assert projectid not in str(project['id'])


@given(u'a project with id {id} exists in the system')
def step_impl(context,id):
    """
    :type context: behave.runner.Context
    :type id: str
    """
    response = requests.get(url+'projects/'+id)
    try:
        assert response.status_code == 200
    except AssertionError:
        newid=0
        while response.status_code != 200 and newid < int(id):
            json_proj = {
                "title": "Office Work",
                "completed": False,
                "active": False,
                "description": "",
                "tasks": []
                }
            new_proj = requests.post(url+'projects',data=json.dumps(json_proj),headers=json_header)
            newid = int(new_proj.json()['id'])
            assert new_proj.status_code == 201 
            response = requests.get(url+'projects/'+id)
        assert response.status_code == 200


@when(u'a user creates a relationship between todo {todoids} and project {projectid} on the project side')
def step_impl(context,todoids,projectid):
    """
    :type context: behave.runner.Context
    :type todoids: str
    :type projectid: str
    """
    todoidlst = todoids.strip().split(',')
    for todoid in todoidlst:
        post = requests.post(url+'projects/'+projectid+'/tasks', data=json.dumps({"id":todoid}), headers=json_header)
        try:
            assert post.status_code == 201  
        except AssertionError:
            assert post.status_code == 404


@then(u'the todo {todoids} will be related to project {projectid}')
def step_impl(context,todoids,projectid):
    """
    :type context: behave.runner.Context
    :type todoids: str
    :type projectid: str
    """
    todoidlst = todoids.strip().split(',')
    for todoid in todoidlst:
        response = requests.get(url+'todos/'+todoid+'/tasksof')
        assert response.status_code == 200
        assert projectid in str(response.json()['projects']) 


@then(u'the project {projectid} will be related to todo {todoids}')
def step_impl(context,projectid,todoids):
    """
    :type context: behave.runner.Context
    :type projectid: str
    :type todoids: str
    """
    response = requests.get(url+'projects/'+projectid+'/tasks')
    assert response.status_code == 200
    todoidlst = todoids.strip().split(',')
    for todoid in todoidlst:
        assert todoid in str(response.json()['todos']) 



@when(u'a user creates a relationship between todo {todoids} and project {projectid} on the todos side')
def step_impl(context,todoids,projectid):
    """
    :type context: behave.runner.Context
    :type todoids: str
    :type projectid: str
    """
    todoidlst = todoids.strip().split(',')
    for todoid in todoidlst:
        post = requests.post(url+'todos/'+todoid+'/tasksof', data=json.dumps({"id":projectid}), headers=json_header)
        try:
            assert post.status_code == 201  
        except:
            #TODO
            assert post.status_code == 404



@then(u'the todo {todoids} will not be related to project {projectid}')
def step_impl(context,todoids,projectid):
    """
    :type context: behave.runner.Context
    :type todoids: str
    :type projectid: str
    """
    todoidlst = todoids.strip().split(',')
    for todoid in todoidlst:
        response = requests.get(url+'todos/'+todoid+'/tasksof')
        for project in response.json()['projects']:
            assert projectid != str(project['id'])


@then(u'the project {projectid} will not be related to todo {todoids}')
def step_impl(context,projectid,todoids):
    """
    :type context: behave.runner.Context
    :type projectid: str
    :type todoids: str
    """
    todoidlst = todoids.strip().split(',')
    for todoid in todoidlst:
        response = requests.get(url+'projects/'+projectid+'/tasks')
        try:
            todos = response.json()['todos']
        except:
            assert True #no todos in project.
        for todo in response.json()['todos']:
            for proj in todo['tasksof']:
                try:
                    assert todoid != str(proj['id'])
                except:
                    print("ERROR: Even if project does not exist, fetching a project returns all existing todos.")
                    assert False
