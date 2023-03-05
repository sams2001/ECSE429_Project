import os
import socket
import subprocess
import time

import requests


def before_all(context):
    context.config.setup_logging()
    jar_path = os.getcwd() + '/runTodoManagerRestAPI-1.5.5.jar'
    subprocess.Popen(["java", "-jar", jar_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def before_scenario(context, scenario):

    jar_path = os.getcwd() + '/runTodoManagerRestAPI-1.5.5.jar'
    subprocess.Popen(["java", "-jar", jar_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    time.sleep(1)


def after_scenario(context, scenario):
    try:
        subprocess.call(['curl', 'http://localhost:4567/shutdown'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except ConnectionError:
        pass
