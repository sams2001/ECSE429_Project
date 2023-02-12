import pytest
import subprocess

@pytest.fixture(scope="session", autouse=True)
def kill_app():
    try:
        process = subprocess.call(['curl', 'http://localhost:4567/shutdown'], shell=True)
    except ConnectionError:
        pass
    

@pytest.fixture(scope='module')
def start_app():
    process =  subprocess.Popen(["java", "-jar", "runTodoManagerRestAPI-1.5.5.jar"], shell=True)
    status_code = subprocess.call(['curl', 'http://localhost:4567'], shell=True)
    while status_code:
        status_code = subprocess.call(['curl', 'http://localhost:4567'], shell=True)
    yield status_code
    kill_app()