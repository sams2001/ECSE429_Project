import requests
from behave import *
import json

url = 'http://localhost:4567/categories'

json_header = {"Content-Type": "application/json"}

