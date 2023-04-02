import os
import subprocess
import time
import pytest
import requests

@pytest.fixture
def resource():
    print("set up")

    try:
        subprocess.call(['curl', 'http://localhost:4567/shutdown'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        path = os.getcwd() + "/runTodoManagerRestAPI-1.5.5.jar"
        process = subprocess.Popen(["java", "-jar", path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        service_running = subprocess.call(['curl', 'http://localhost:4567'])

        while service_running:
            service_running = subprocess.call(['curl', 'http://localhost:4567'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        yield process

    finally:
        print("tear down")
        subprocess.call(['curl', 'http://localhost:4567/shutdown'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        process.kill()

