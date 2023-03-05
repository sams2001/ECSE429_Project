import os
import subprocess


def before_scenario(context, scenario):
    try:
        path = os.getcwd() + '/Part B/runTodoManagerRestAPI-1.5.5.jar'
        process = subprocess.Popen(["java", "-jar", path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        service_running = subprocess.call(['curl', 'http://localhost:4567'])

        while service_running:
            service_running = subprocess.call(['curl', 'http://localhost:4567'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        yield process
    finally:
        subprocess.call(['curl', 'http://localhost:4567/shutdown'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        process.kill()


def after_all(context):
    subprocess.call(['curl', 'http://localhost:4567/shutdown'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
