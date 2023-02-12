
import requests
import json

url = 'http://localhost:4567/projects'

json_payload = """
{
    "title": "Home Activities",
    "completed": False,
    "active": False,
    "description": ""
}"""

json_header = {"Content-Type": "application/json"}


def test_projects_header():
    response = requests.head(url)
    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json'

def test_get_projects():
    response = requests.get(url)
    assert response.status_code == 200
    assert 'projects' in response.json()

def test_get_project():
    response = requests.get(url+'/1')
    assert response.status_code == 200
    assert 'projects' in response.json()

def test_get_project_failure():
    response = requests.get(url+'/1000')
    assert response.status_code == 404
    assert 'errorMessages' in response.json()

def test_post_project_json():
    response = requests.post(url,data=json_payload,headers=json_header)
    assert response.status_code == 201 #Create
    projects = requests.get(url).json()["projects"]
    assert response.json() in projects

def test_delete_task():
    response = requests.delete(url + "/1/tasks/1")
    assert response.status_code == 200

def test_delete_task():
    response = requests.delete(url + "/1/tasks/1000")
    assert response.status_code == 404

def test_delete_project():
    post = requests.post(url,data=json_payload,headers=json_header)
    id_to_delete = post.json()["id"]
    response = requests.delete(url + "/"+id_to_delete)
    assert response.status_code == 200

def test_delete_project_failure():
    response = requests.delete(url + "/1000")
    assert response.status_code == 404


