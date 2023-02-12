#!/bin/bash

java -jar ../runTodoManagerRestAPI-1.5.5.jar


printf "Getting all projects \n"

curl -X GET "http://localhost:4567/projects"

printf "\n Done. \n"


printf "Getting project with id=1 \n"

curl -X GET "http://localhost:4567/projects/1"

printf "\n Done. \n"


printf "Creating project \n"

curl -X POST "http://localhost:4567/projects" -H "Content-Type: application/json" -d '
{
    "title": "Home Activities",
    "completed": false,
    "active": false,
    "description": ""
}'

printf "\n Done. \n"


printf "Deleting task by project \n"

curl -I -X DELETE "http://localhost:4567/projects/1/tasks/1"

printf "\n Done. \n"


printf "Deleting project \n"

post_response=$(curl -X POST "http://localhost:4567/projects" -H "Content-Type: application/json" -d '
{
    "title": "Home Activities",
    "completed": false,
    "active": false,
    "description": ""
}')

id_to_delete=$(echo "$post_response" | jq '.id')

curl -I -X DELETE "http://localhost:4567/projects/$id_to_delete"

printf "\n Done. \n"


printf "shutting down app... \n"

curl http://localhost:4567/shutdown
