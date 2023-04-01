import pytest
import requests
import os
import psutil
from time import sleep

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
create, delete or change project object at different states
"""


def projects_setup_empty():
    projects = requests.get(projects_url).json()['projects']
    while(len(projects) != 1):
        for i in range(1,len(projects)): #delete all but one.. basically empty
            projects = projects[i]
            request = requests.delete(projects_url + "/" + projects['id'])
        todos = requests.get(projects_url).json()['projects']

def populate_helper(num_to_reach):
    projects = requests.get(projects_url).json()['projects']
    num_projects = len(projects)
    while(len(projects) != num_to_reach):
        if (num_projects>num_to_reach):
            for i in range(num_projects-num_to_reach): 
                projects = projects[i]
                request = requests.delete(projects_url + "/" + projects['id'])
        else:
            for i in range(num_to_reach-num_projects):
                response = requests.post(projects_url,data=json_payload_projects,headers=json_header)
        projects = requests.get(projects_url).json()['projects']

    #assert len(projects) == num_to_reach


def projects_setup_half_populated():
    populate_helper(50)

def projects_setup_populated():
    populate_helper(100) 

def projects_setup_very_populated():
    populate_helper(500)


def test_control():
    print()
    print("==============================================================  Control  ===============================================================")
    process = psutil.Process(os.getpid())
    print('The CPU usage is: ', psutil.cpu_percent(0.5))
    print('RAM Used (GB):', str(process.memory_info().rss))



def test_post_projects():
    process = psutil.Process(os.getpid())
    print('The CPU usage is: ', psutil.cpu_percent(0.5))
    response = requests.post(projects_url,data=json_payload_projects,headers=json_header)
    print('RAM Used (GB):', str(process.memory_info().rss))
    assert response.status_code == 201
    sleep(0.2)


def test_delete_projects():
    process = psutil.Process(os.getpid())
    projects = requests.get(projects_url).json()['projects']
    project_id = projects[0]['id']
    print('The CPU usage is: ', psutil.cpu_percent(0.5))
    delete = requests.delete(projects_url + "/" + project_id)
    print('RAM Used (GB):', str(process.memory_info().rss))
    assert delete.status_code == 200
    sleep(0.2)


def test_update_projects():
    process = psutil.Process(os.getpid())
    projects = requests.get(projects_url).json()['todos']
    project_id = projects[0]['id']
    print('The CPU usage is: ', psutil.cpu_percent(0.5))
    update = requests.put(projects_url + '/' + project_id,data=json_payload_projects_new,headers=json_header)
    print('RAM Used (GB):', str(process.memory_info().rss))
    assert update.status_code == 200
    sleep(0.2)


if __name__ == "__main__":
    test_control()
    print()
    print("==============================================================  Empty  ===============================================================")
    projects_setup_empty()
    print("POST request:")
    test_post_projects()
    print()
    print("PUT request:")
    test_update_projects()
    print()
    print("DELETE request:")
    test_delete_projects() 
    
    print()
    print("============================================================  50 in system  ==============================================================")
    
    projects_setup_half_populated()
    print("POST request:")
    test_post_projects()
    print()
    print("PUT request:")
    test_update_projects()
    print()
    print("DELETE request:")
    test_delete_projects() 
    
    print()
    print("==============================================================  100 in system  ===============================================================")
    
    projects_setup_populated()
    print("POST request:")
    test_post_projects()
    print()
    print("PUT request:")
    test_update_projects()
    print()
    print("DELETE request:")
    test_delete_projects() 
        
    print()
    print("==============================================================  500 in system  ===============================================================")
    
    projects_setup_very_populated()
    print("POST request:")
    test_post_projects()
    print()
    print("PUT request:")
    test_update_projects()
    print()
    print("DELETE request:")
    test_delete_projects() 
    