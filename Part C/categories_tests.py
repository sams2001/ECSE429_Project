import csv
import os
import time
import requests
import psutil

url = "http://localhost:4567/categories"

json_payload = """{
        "title": "School",
        "description": "testing"
        }"""

json_payload_new = """{
        "title": "School",
        "description": "exam"
        }"""

json_header = {"Content-Type": "application/json"}

def test_performance_create_category():

    num_objects = [10, 50, 100, 500, 1000]
    transaction_time = []
    cpu_percent = []
    memory_available = []

    for n in num_objects:

        process = psutil.Process(os.getpid())
        start_cpu_percent = process.cpu_percent(0.5)
        start_memory = process.memory_info().rss / 1024 / 1024
        start_time = time.time()

        for i in range(n):

            # Create an object with random data
            # Example code for creating a category with random data
            # title = f"Category {i}"
            # description = f"This is category {i}"
            # json_payload = f'{{"title": "{title}", "description": "{description}"}}'
            response = requests.post(url, data=json_payload, headers=json_header)
            assert response.status_code == 201

        end_time = time.time()
        end_cpu_percent = process.cpu_percent(0.5)
        end_memory = process.memory_info().rss / 1024 / 1024

        delta_time = end_time - start_time
        delta_cpu_percent = end_cpu_percent - start_cpu_percent
        delta_memory = end_memory - start_memory

        transaction_time.append(delta_time)
        cpu_percent.append(end_cpu_percent)
        memory_available.append(end_memory)

    create_category_file = open(os.path.join("test_data", "create_category_file.csv"), "w", newline='')
    writer = csv.writer(create_category_file)
    writer.writerow(num_objects)
    writer.writerow(transaction_time)
    writer.writerow(cpu_percent)
    writer.writerow(memory_available)


def test_performance_delete_category():

    num_objects = [10, 50, 100, 500, 1000]
    transaction_time = []
    cpu_percent = []
    memory_available = []

    for n in num_objects:

        # Create n objects to delete
        for i in range(n):
            # title = f"Category {i}"
            # description = f"This is category {i}"
            # json_payload = f'{{"title": "{title}", "description": "{description}"}}'
            response = requests.post(url, data=json_payload, headers=json_header)
            assert response.status_code == 201

        process = psutil.Process(os.getpid())
        start_cpu_percent = process.cpu_percent(0.5)
        start_memory = process.memory_info().rss / 1024 / 1024
        start_time = time.time()

        for i in range(n):
            to_delete = requests.get(url).json()['categories'][0]['id']
            response = requests.delete(url + "/" + str(to_delete))
            assert response.status_code == 200

        end_time = time.time()
        end_cpu_percent = process.cpu_percent(0.5)
        end_memory = process.memory_info().rss / 1024 / 1024

        delta_time = end_time - start_time
        delta_cpu_percent = end_cpu_percent - start_cpu_percent
        delta_memory = end_memory - start_memory

        transaction_time.append(delta_time)
        cpu_percent.append(end_cpu_percent)
        memory_available.append(end_memory)

    create_category_file = open(os.path.join("test_data", "delete_category_file.csv"), "w", newline='')
    writer = csv.writer(create_category_file)
    writer.writerow(num_objects)
    writer.writerow(transaction_time)
    writer.writerow(cpu_percent)
    writer.writerow(memory_available)


def test_performance_update_category():
    
    num_objects = [10, 50, 100, 500, 1000]
    transaction_time = []
    cpu_percent = []
    memory_available = []

    for n in num_objects:
        # Create n objects to update
        for i in range(n):
            # title = f"Category {i}"
            # description = f"This is category {i}"
            # json_payload = f'{{"title": "{title}", "description": "{description}"}}'
            response = requests.post(url, data=json_payload, headers=json_header)
            assert response.status_code == 201
        
        process = psutil.Process(os.getpid())
        start_cpu_percent = process.cpu_percent(0.5)
        start_memory = process.memory_info().rss / 1024 / 1024
        start_time = time.time()

        for i in range(n):
            # title = f"New Category {i}"
            # description = f"This is the updated category {i}"
            # json_payload = f'{{"title": "{title}", "description": "{description}"}}'
            to_update = requests.get(url).json()['categories'][0]['id']
            response = requests.put(url + "/" + str(to_update), data=json_payload_new, headers=json_header)
            assert response.status_code == 200
        
        end_time = time.time()
        end_cpu_percent = process.cpu_percent(0.5)
        end_memory = process.memory_info().rss / 1024 / 1024

        delta_time = end_time - start_time
        delta_cpu_percent = end_cpu_percent - start_cpu_percent
        delta_memory = end_memory - start_memory

        transaction_time.append(delta_time)
        cpu_percent.append(end_cpu_percent)
        memory_available.append(end_memory)

    create_category_file = open(os.path.join("test_data", "update_category_file.csv"), "w", newline='')
    writer = csv.writer(create_category_file)
    writer.writerow(num_objects)
    writer.writerow(transaction_time)
    writer.writerow(cpu_percent)
    writer.writerow(memory_available)

def categories_setup_empty():
    categories = requests.get(url).json()['categories']
    if len(categories) > 0:
        for i in range(0,len(categories)): #delete all but one.. basically empty
            category = categories[i]
            requests.delete(url + "/" + category['id'])
        categories_after_delete = requests.get(url).json()['categories']
        if len(categories_after_delete) == 0:
            return
    else:
        return

if __name__ == "__main__":

    categories_setup_empty()
    test_performance_create_category()

    categories_setup_empty()
    test_performance_delete_category()

    categories_setup_empty()
    test_performance_update_category()