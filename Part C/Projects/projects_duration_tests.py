import pytest
import requests
import psutil
import os
from time import sleep

#Run tests with `pytest --durations=0 projects_tests.py` to see the duration of each test

projects_url = 'http://localhost:4567/projects'

json_payload_projects = """
{
    "title": "Home Activities",
    "completed": False,
    "active": False,
    "description": ""
}"""
json_payload_projects_new = """
{
    "title": "Work Activities",
    "completed": False,
    "active": False,
    "description": ""
}"""

json_header = {"Content-Type": "application/json"}

"""
create, delete or change projects object at different states
"""

#empty state setup
@pytest.fixture
def projects_setup_empty(resource):
    projects = requests.get(projects_url).json()['projects']
    while(len(projects) != 1):
        for i in range(1,len(projects)): #delete all but one.. basically empty
            project = projects[i]
            request = requests.delete(projects_url + "/" + project['id'])
        projects = requests.get(projects_url).json()['projects']
    assert len(requests.get(projects_url).json()['projects']) == 1


def populate_helper(num_to_reach):
    projects = requests.get(projects_url).json()['projects']
    num_projects = len(projects)
    while(len(projects) != num_to_reach):
        if (num_projects>num_to_reach):
            for i in range(num_projects-num_to_reach): 
                project = projects[i]
                request = requests.delete(projects_url + "/" + project['id'])
        else:
            for i in range(num_to_reach-num_projects):
                response = requests.post(projects_url,data=json_payload_projects,headers=json_header)
        projects = requests.get(projects_url).json()['projects']

    assert len(projects) == num_to_reach

@pytest.fixture
def projects_setup_half_populated(resource):
    populate_helper(50)

@pytest.fixture
def projects_setup_populated(resource):
    populate_helper(100) 

@pytest.fixture
def projects_setup_very_populated(resource):
    populate_helper(500)


@pytest.mark.parametrize('state', ['projects_setup_very_populated', 'projects_setup_populated', 'projects_setup_half_populated', 'projects_setup_empty'])
def test_post_projects(resource, state):
    process = psutil.Process(os.getpid())
    response = requests.post(projects_url,data=json_payload_projects,headers=json_header)
    print('The CPU usage is: ', process.cpu_percent(0.5))
    print('RAM Used (GB):', str(process.memory_info().rss))

    assert response.status_code == 201
    sleep(0.1) #cpu takes 0.5s sample - make sure there's no overlap with other function calls


@pytest.mark.parametrize('state', ['projects_setup_very_populated', 'projects_setup_populated', 'projects_setup_half_populated', 'projects_setup_empty'])
def test_delete_projects(resource,state):
    process = psutil.Process(os.getpid())
    projects = requests.get(projects_url).json()['projects']
    project_id = projects[0]['id']
    delete = requests.delete(projects_url + "/" + project_id)
    print('The CPU usage is: ', process.cpu_percent(0.5))
    print('RAM Used (GB):', str(process.memory_info().rss))

    assert delete.status_code == 200
    sleep(0.1) #cpu takes 0.5s sample - make sure there's no overlap with other function calls


@pytest.mark.parametrize('state', ['projects_setup_very_populated', 'projects_setup_populated', 'projects_setup_half_populated', 'projects_setup_empty'])
def test_update_projects(resource,state):
    process = psutil.Process(os.getpid())
    projects = requests.get(projects_url).json()['projects']
    project_id = projects[0]['id']
    update = requests.put(projects_url + '/' + project_id,data=json_payload_projects_new,headers=json_header)
    print('The CPU usage is: ', process.cpu_percent(0.5))
    print('RAM Used (GB):', str(process.memory_info().rss))
    
    assert update.status_code == 200
    sleep(0.1)
