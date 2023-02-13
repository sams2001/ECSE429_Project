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

xml_faulty_payload = """
<category> 
    <description> yes this is a description </description> 
</category>
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

def test_get_category():
    response = requests.get(url+'/1')
    assert response.status_code == 200
    assert 'categories' in response.json()

def test_get_category_failure():
    number_categories_pre = len(requests.get(url).json()["categories"])
    response = requests.get(url+'/0')
    assert response.status_code == 404
    assert 'errorMessages' in response.json()
    number_categories_post = len(requests.get(url).json()["categories"])
    assert number_categories_post == number_categories_pre

def test_post_category_json():
    response = requests.post(url,data=json_payload,headers=json_header)
    assert response.status_code == 201 #Create
    categories = requests.get(url).json()["categories"]
    assert response.json() in categories

def test_post_category_json_duplicate():
    response = requests.post(url,data=json_payload,headers=json_header)
    assert response.status_code == 201 #Create duplicate
    categories = requests.get(url).json()["categories"]
    assert response.json() in categories

def test_post_category_json_fail():
    number_categories_pre = len(requests.get(url).json()["categories"])
    response = requests.post(url,data="",headers=json_header)
    assert response.status_code == 400 
    assert 'errorMessages' in response.json()
    number_categories_post = len(requests.get(url).json()["categories"])
    assert number_categories_post == number_categories_pre


def test_put_category_json():
    response = requests.put(url+'/2',data=json_payload, headers=json_header)
    assert response.status_code == 200 

def test_put_category_json_failure():
    response = requests.put(url+'/0',data=json_payload, headers=json_header)
    assert response.status_code == 404 

def test_delete_category():
    post = requests.post(url,data=json_payload,headers=json_header)
    id_to_delete = post.json()["id"]
    number_categories_pre = len(requests.get(url).json()["categories"])
    response = requests.delete(url + "/"+id_to_delete)
    assert response.status_code == 200
    number_categories_post = len(requests.get(url).json()["categories"])
    assert number_categories_post == number_categories_pre -1

def test_delete_category_failure():
    number_categories_pre = len(requests.get(url).json()["categories"])
    response = requests.delete(url + "/1000")
    assert response.status_code == 404
    number_categories_post = len(requests.get(url).json()["categories"])
    assert number_categories_pre == number_categories_post

def test_post_category_xml():
    number_categories_pre = len(requests.get(url).json()["categories"])
    response = requests.post(url, headers=xml_headers, data=xml_payload)
    assert response.status_code == 201
    number_categories_post = len(requests.get(url).json()["categories"])
    assert number_categories_pre +1 == number_categories_post 

def test_post_category_faulty_xml():
    number_categories_pre = len(requests.get(url).json()["categories"])
    response = requests.post(url, headers=xml_headers, data=xml_faulty_payload)
    assert 'field is mandatory' in str(response.json())
    number_categories_post = len(requests.get(url).json()["categories"])
    assert number_categories_pre == number_categories_post 

def test_put_category_xml():
    response = requests.put(url+"/2", headers=xml_headers, data=xml_payload)
    assert response.status_code == 200

def test_put_category_xml_failure():
    response = requests.put(url+"/1000", headers=xml_headers, data=xml_payload)
    assert response.status_code == 404