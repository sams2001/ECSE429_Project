import requests

url = "http://localhost:4567/"

xml_headers = {'Content-Type': 'application/xml'}

xml_payload = """
<category> 
    <description> yes this is a description </description> 
    <title> this is the title </title>
</category>
"""

json_payload = """
    "categories": [
        {
            "id": "1",
            "title": "Office",
            "description": ""
        }
    ]
"""

def test_post_project_categories_xml():
    response = requests.put(url+"/2/projects", headers=xml_headers, data=xml_payload)
    assert response.status_code == 404

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

def test_delete_category_todo():
    response = requests.delete("http://localhost:4567/todos/:id/categories/:id")
    assert response.status_code == 404

def test_delete_category_todo():
    response = requests.delete("http://localhost:4567/todos/1/categories/1")
    assert response.status_code == 200

def test_get_categories_by_todoId():
    response = requests.get('http://localhost:4567/todos/1/categories/1')
    assert response.status_code == 404

def test_get_todos_by_category_unspecified():
    response = requests.get('http://localhost:4567/projects/:id/tasks')
    assert response.status_code == 200

