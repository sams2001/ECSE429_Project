import requests
from behave import *
import json

url = 'http://localhost:4567/'

json_header = {"Content-Type": "application/json"}

app_project = requests.Response

@given(u'a category with id {catids} exist in the system')
def step_impl(context, catids):
    """
    :type context: behave.runner.Context
    :type todoids: str
    """
    catislst = catids.strip().split(',')
    for id in catislst:
        response = requests.get(url+'categories/'+id)
        if response.status_code == 404:
            newid=0
            while response.status_code != 200 and newid < int(id):
                category = {
                 "title": "Homework",
                 "description": "All assignments and projects",
                 "projects": [
                        {
                        "id": "1"
                        }
                    ]
                 }
                response1 = requests.post(url+"categories", data=json.dumps(category), headers=json_header)
                newid = int(response1.json()['id'])
                assert response1.status_code == 201 
                response = requests.get(url+'categories/'+id)


        response = requests.get(url+'categories/'+id)
        assert response.status_code == 200


    # response = requests.get(url+'/'+"categories"+'/'+catid)
    # if response.status_code == 404:
    #     category = {
    #     "title": "Homework",
    #     "description": "All assignments and projects"
    #     }
    #     requests.post(url, data=json.dumps(category), headers=json_header)
    #     response = requests.get(url+'/'+"categories"+'/'+catid)

    # assert response.status_code == 200


@given(u'a project with id {projectid} exists with related category {catids}')
def step_impl(context, projectid, catids):
    """
    :type context: behave.runner.Context
    :type projectid: str
    :type taskids: str
    """
    catidlst = catids.strip().split(",")

    response = requests.get(url+'projects/'+projectid)
    if response.status_code == 200:
        for catid in catidlst:
            try:
                response = requests.get(url+'projects/'+projectid+'/categories')
                assert catid in str(response.json())
            except AssertionError:
                post = requests.post(url+'projects/'+projectid+'/categories', data=json.dumps({"id":catid}), headers=json_header)
                assert post.status_code == 201
                response = requests.get(url+'projects/'+projectid+'/categories')
                assert catid in str(response.json())

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
        for catid in catidlst:
            post2 = requests.post(url+'projects/'+projectid+'/categories', data=json.dumps({"id":catid}), headers=json_header)
            assert post2.status_code == 201
    else:
        assert False
    # response = requests.get(url+'/'+"projects"+'/'+projectid)
    # if response.status_code == 404:
    #     project_json = {
    #     "title": "Big Proj 1",
    #     "description": "relating to registering for courses",
    #     "completed": json.loads("false"),
    #     "active": json.loads("true"),
    #     "categories": 
    #     }
    #     requests.post(url, data=json.dumps(project_json), headers=json_header)
    #     response = requests.get(url+'/'+id)

    # assert response.status_code == 200
    # assert id == response.json()["projects"][0]['id']


@when(u'a user fetches the category via providing the project id {projectid}')
def step_impl(context, projectid):
    """
    :type context: behave.runner.Context
    :type projectid: str
    """
    global app_project
    app_project = requests.get(url+'projects/'+projectid+'/categories')
    #found or not found, no other status codes
    try:
        assert app_project.status_code == 200
    except:
        assert app_project.status_code == 404


@then(u'the system will return all categories relating to the project, as well as the corresponding id {catids}')
def step_impl(context, catids):
    """
    :type context: behave.runner.Context
    :type taskids: str
    :type projectid: str
    """
    global app_project
    catidlst = catids.strip().split(',')
    
    for catid in catidlst:
        assert catid in str(app_project.json())


@given(u'their is at least one project in the system with associated categories')
def step_impl(context):
    """
    :type context: behave.runner.Context
    :type projectid: str
    :type taskids: str
    """
    r1 = requests.get(url+'projects')
    if r1.status_code == 404:
        project_payload = {
            "title": "Work",
            "completed": False,
            "active": False,
            "description": "",
            "tasks": []
            }
        r1 = requests.post(url+'projects', data=json.dumps(project_payload), headers=json_header)
        assert r1.status_code == 201

    r2 = requests.get(url+'categories')
    if r2.status_code == 404:
        category = {
         "title": "Homework",
         "description": "All assignments and projects"
         }
        r2 = requests.post(url+'category', data=json.dumps(category), headers=json_header)
        assert r2.status_code == 201

    response = requests.get(url+'projects/:id/categories')
    if response.json()["categories"][0] is None:
        post2 = requests.post(url+'projects/1/categories', data=json.dumps({"id":1}), headers=json_header)
        assert post2.status_code == 201


@when(u'a user fetches the categories of a project without specifying the project id')
def step_impl(context):
    global app_project
    app_project = requests.get(url+'projects/:id/categories')
    assert app_project.status_code != 404


@then(u'the system will return all categories in the system that have relationships with any project as well as the corresponding id')
def step_impl(context):
    global app_project
    assert str(app_project.json()) is not None


@when(u'a user elects to fetch all categories related to a project by providing the {incorrectId}')
def step_impl(context, incorrectId):
    global app_project
    app_project = requests.get(url+'projects/'+incorrectId+'/categories')
    assert app_project.status_code != 404