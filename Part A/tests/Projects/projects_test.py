import pytest
import requests
import json
import subprocess

url = 'http://localhost:4567/projects'

def test_projects_header():
    response = requests.head(url)
    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json'

def test_get_projects():
    response = requests.get(url)
    assert response.status_code == 200
    assert 'projects' in response.json()

def test_get_projects():
    response = requests.get(url+'/1')
    assert response.status_code == 200
    assert 'projects' in response.json()

def test_get_projects():
    response = requests.get(url+'/1000')
    assert response.status_code == 404
    assert 'errorMessages' in response.json()

def test_post_project_json():
    new_project_json = json.dumps({
        "title": "Home Activities",
        "completed": False,
        "active": False,
        "description": ""
        })
    response = requests.post(url,data=new_project_json,headers={"Content-Type": "application/json"})
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
    response = requests.delete(url + "/2")
    assert response.status_code == 200

def test_delete_project_failure():
    response = requests.delete(url + "/1000")
    assert response.status_code == 404


