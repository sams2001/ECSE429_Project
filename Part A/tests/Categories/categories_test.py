import requests


url = "http://localhost:4567/categories"

xml_payload = """
<category> 
    <description> yes this is a description </description> 
    <title> this is the title </title>
</category>
"""

json_payload = """{
        "title": "School",
        "description": "testing"
        }"""

json_header = {"Content-Type": "application/json"}

xml_payload2 = """
<project>
    <active>false</active>
    <description>atat non proident, s</description>
    <id>2</id>
    <completed>false</completed>
    <title>non proident, sunt i</title>
</project>
"""

xml_headers = {'Content-Type': 'application/xml'}

def test_categories_header():
    response = requests.head('http://localhost:4567/categories')
    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json'

def test_get_categories():
    response = requests.get(url)
    assert response.status_code == 200
    assert 'categories' in response.json()

def test_get_categories_failure():
    response = requests.get(url+'/0')
    assert response.status_code == 404
    assert 'errorMessages' in response.json()

def test_post_category_json():
    response = requests.post(url,data=json_payload,headers=json_header)
    assert response.status_code == 201 #Create
    categories = requests.get(url).json()["categories"]
    assert response.json() in categories

def test_post_category_json():
    response = requests.post(url,data=json_payload,headers=json_header)
    assert response.status_code == 201 #Create duplicate
    categories = requests.get(url).json()["categories"]
    assert response.json() in categories

def test_put_category_json():
    response = requests.put(url+'/2',data=json_payload, headers=json_header)
    assert response.status_code == 200 #Create

def test_put_category_json_failure():
    response = requests.put(url+'/0',data=json_payload, headers=json_header)
    assert response.status_code == 404 #Create

def test_delete_category():
    response = requests.delete(url + "/1")
    assert response.status_code == 200

def test_delete_category_failure():
    response = requests.delete(url + "/1000")
    assert response.status_code == 404

def test_post_category_xml():
    response = requests.post(url, headers=xml_headers, data=xml_payload)
    assert response.status_code == 201

def test_post_category_xml_fail():
    response = requests.post(url+"/1", headers=xml_headers, data=xml_payload)
    assert response.status_code == 404

def test_put_category_xml():
    response = requests.put(url+"/2", headers=xml_headers, data=xml_payload)
    assert response.status_code == 200

def test_post_project_categories_xml():
    response = requests.put(url+"/2/projects", headers=xml_headers, data=xml_payload2)
    assert response.status_code == 405

