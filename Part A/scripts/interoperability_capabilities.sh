#!/bin/bash

java -jar ../runTodoManagerRestAPI-1.5.5.jar

printf "Geting todos by category \n"

curl http://localhost:4567/categories/1/todos

printf "\n Done. \n"

printf "Getting categories by todo \n"

curl http://localhost:4567/todos/1/categories

printf "\n Done. \n"

printf "Getting all todos and their category \n"

curl -I -X GET "http://localhost:4567/todos/:id/categories"

printf "\n Done. \n"

printf "Deleting todo by category \n"

curl -I -X DELETE "http://localhost:4567/todos/1/categories/1"

printf "\n Done. \n"

printf "Getting all projects and their tasks \n"

curl -I -X GET "http://localhost:4567/projects/:id/tasks"

printf "\n Done. \n"

printf "shutting down app... \n"

curl http://localhost:4567/shutdown

