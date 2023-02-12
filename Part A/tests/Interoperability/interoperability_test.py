import requests
import json

url = "http://localhost:4567/"

xml_headers = {'Content-Type': 'application/xml'}

xml_payload = """
<category> 
    <description> yes this is a description </description> 
    <title> this is the title </title>
</category>
"""

json_header = {"Content-Type": "application/json"}

json_payload = """
    "categories": [
        {
            "id": "1",
            "title": "Office",
            "description": ""
        }
    ]
"""

json_project_payload = """
{
    "title": "Home Activities",
    "completed": False,
    "active": False,
    "description": ""
}"""

json_category_payload = """{
        "title": "School",
        "description": "testing"
        }"""

json_todo_payload = """
{
    "title": "submit paperwork",
    "doneStatus": False,
    "description": ""
}
"""

def test_post_project_categories_json():
    post = requests.post(url+"categories",data=json_category_payload,headers=json_header)
    id_to_use = post.json()["id"]
    response = requests.post(url+"categories/"+id_to_use+"/projects", headers=json_header, data=json_category_payload)
    assert response.status_code == 201

def test_post_category_project():
    post = requests.post(url+"projects",data=json_project_payload,headers=json_header)
    id_to_use = post.json()["id"]
    post2 = requests.post(url+"categories",data=json_category_payload,headers=json_header)
    id_category = post2.json()["id"]    
    json_body = json.dumps({
    "id": f"{id_category}",
    })
    response = requests.post(url+"projects/"+id_to_use+"/categories", headers=json_header, data=json_body)
    assert response.status_code == 201

def test_post_project_categories_xml():
    post = requests.post(url+"categories",data=json_category_payload,headers=json_header)
    id_to_use = post.json()["id"]
    response = requests.post(url+"categories/"+id_to_use+"/projects", headers=xml_headers, data=xml_payload)
    assert response.status_code == 201

def test_post_project_categories_failure():
    post = requests.post(url+"projects",data=json_project_payload,headers=json_header)
    id_to_use = post.json()["id"]
    response = requests.post(url+"projects/"+id_to_use+"/categories", headers=json_header, data=json_payload)
    assert response.status_code == 400

def test_post_category_todo():
    post = requests.post(url+"todos",data=json_todo_payload,headers=json_header)
    id_todo = post.json()["id"]
    post2 = requests.post(url+"categories",data=json_category_payload,headers=json_header)
    id_category = post2.json()["id"]
    json_body = json.dumps({
        "id": f"{id_category}",
        })
    post3 = requests.post("http://localhost:4567/todos/"+id_todo+"/categories", data=json_body, headers=json_header)
    assert post3.status_code == 201

def test_post_category_todo_fail():
    json_body = json.dumps({
        "id": "10000",
        })
    post3 = requests.post("http://localhost:4567/todos/1/categories", data=json_body, headers=json_header)
    assert post3.status_code == 404

def test_post_todo_category():
    post = requests.post(url+"todos",data=json_todo_payload,headers=json_header)
    id_todo = post.json()["id"]
    post2 = requests.post(url+"categories",data=json_category_payload,headers=json_header)
    id_category = post2.json()["id"]
    json_body = json.dumps({
        "id": f"{id_todo}",
        })
    post3 = requests.post("http://localhost:4567/categories/"+id_category+"/todos", data=json_body, headers=json_header)
    assert post3.status_code == 201

def test_post_todo_category_fail():
    json_body = json.dumps({
        "id": "10000",
        })
    post3 = requests.post("http://localhost:4567/categories/1/todos", data=json_body, headers=json_header)
    assert post3.status_code == 404


def test_get_todos_by_category():
    response = requests.get('http://localhost:4567/categories/1/todos')
    todos = requests.get('http://localhost:4567/todos').json()["todos"]
    todos_in_category = [i for i in todos if 'categories' in i.keys() and {'id': '1'} in i['categories']]
    
    assert response.status_code == 200

    #from the original entries, todo 1 is in category 1 and todo 2 is not.
    print(requests.get('http://localhost:4567/todos/1').json()["todos"])
    print(todos_in_category)
    assert requests.get('http://localhost:4567/todos/1').json()["todos"][0] in todos_in_category
    assert requests.get('http://localhost:4567/todos/2').json()["todos"][0] not in todos_in_category

def test_get_categories_by_todos():
    response = requests.get('http://localhost:4567/todos/1/categories').json()["categories"]
    category = requests.get('http://localhost:4567/categories/1').json()["categories"][0]
    #from the original entries, todo 1 has category 1. if more categories are added, 
    # should still be valid, so just check that category 1 is still in todo 1's categories, not if they are equal
    assert category in response

def test_get_category_todo():
    response = requests.get('http://localhost:4567/todos/:id/categories')
    assert response.status_code == 200

def test_delete_category_todo_unspecified():
    response = requests.delete("http://localhost:4567/todos/:id/categories/:id")
    assert response.status_code == 404

def test_delete_category_todo():
    post = requests.post(url+"todos",data=json_todo_payload,headers=json_header)
    id_todo = post.json()["id"]
    post2 = requests.post(url+"categories",data=json_category_payload,headers=json_header)
    id_category = post2.json()["id"]
    json_body = json.dumps({
        "id": f"{id_category}",
        })
    post3 = requests.post("http://localhost:4567/todos/"+id_todo+"/categories", data=json_body, headers=json_header)
    response = requests.delete(url+ "todos/"+id_todo+"/categories/"+id_category)
    assert response.status_code == 200

def test_get_categories_by_todoId():
    response = requests.get(url+'todos/1/categories/1')
    assert response.status_code == 404

def test_get_todos_by_category_unspecified():
    response = requests.get(url+'projects/:id/tasks')
    assert response.status_code == 200

def test_delete_projects_tasks_unspecified_failure():
    response = requests.delete(url+"projects/:id/tasks/:id")
    assert response.status_code == 404

def test_delete_task():
    post = requests.post(url+"todos",data=json_todo_payload,headers=json_header)
    id_todo = post.json()["id"]
    post2 = requests.post(url+"projects",data=json_project_payload,headers=json_header)
    id_projects = post2.json()["id"]
    json_body = json.dumps({
        "id": f"{id_todo}",
        })
    post3 = requests.post(url+ f"projects/{id_projects}/tasks", data=json_body, headers=json_header)
    response = requests.delete(url + f"projects/{id_projects}/tasks/{id_todo}")
    assert response.status_code == 200

def test_delete_task_failure():
    response = requests.delete(url + "projects/1/tasks/1000")
    assert response.status_code == 404
