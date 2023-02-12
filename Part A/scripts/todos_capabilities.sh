#!/bin/bash

java -jar ../runTodoManagerRestAPI-1.5.5.jar

printf "Getting all todos \n"

curl -X GET "http://localhost:4567/todos"

printf "\n Done. \n"


printf "Creating todo \n"

curl -X POST -H "Content-Type: application/json" -d '{"title": "submit paperwork", "doneStatus": False, "description": ""}' "http://localhost:4567/todos"

printf "\n Done. \n"


printf "Getting todo with id=1"

curl -X GET "http://localhost:4567/todos/1"

printf "\n Done. \n"


printf "Deleting todo \n"

curl -X POST -H "Content-Type: application/json" -d '{
    "title": "submit paperwork",
    "doneStatus": False,
    "description": ""
}' "http://localhost:4567/todos"

id_to_delete=$(curl -X POST -H "Content-Type: application/json" -d '{
    "title": "submit paperwork",
    "doneStatus": False,
    "description": ""
}' "http://localhost:4567/todos" | awk '{print $6}' | awk -F'"' '{print $2}')

curl -X DELETE "http://localhost:4567/todos/$id_to_delete"

printf "\n Done. \n"


printf "shutting down app... \n"

curl http://localhost:4567/shutdown
