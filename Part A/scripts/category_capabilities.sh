#!/bin/bash

java -jar ../runTodoManagerRestAPI-1.5.5.jar

printf "Creating new category \n"

curl -X POST -H "Content-Type: application/json" -d '{
        "title": "School",
        "description": "testing"
        }' http://localhost:4567/categories

printf "\n Done. \n"

printf "Creating duplicate category \n"

curl -X POST -H "Content-Type: application/json" -d '{
        "title": "School",
        "description": "testing"
        }' http://localhost:4567/categories

printf "\n Done. \n"

printf "Get all categories \n"

curl http://localhost:4567/categories

printf "\n Done. \n"

printf "Get category id=1 \n"

curl http://localhost:4567/categories/1

printf "\n Done. \n"

printf "Re-labeling category \n"

curl -X PUT -H "Content-Type: application/json" -d '{
        "title": "School",
        "description": "testing"
        }' http://localhost:4567/categories/2

printf "\n Done. \n"

printf "Deleting category \n"

curl -X DELETE http://localhost:4567/categories/1

printf "\n Done. \n"

printf "shutting down app... \n"

curl http://localhost:4567/shutdown
