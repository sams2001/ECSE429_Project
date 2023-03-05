Feature: Update a pre-existing project's field/s

    As a user, I want to update a project's fields, so that I do not have to delete and create a new project.

    Background:
        Given the application is running

    #Normal Flow
    Scenario Outline: Update a project's string fields
        Given a project with id "<id>" exists
        When a user initiates the update of the project with id "<id>" to title "<title>", completed status "<completedStatus>", active status "<activeStatus>", and description "<description>"
        Then the project with id "<id>" will have title "<title>", completed status "<completedStatus>", active status "<activeStatus>", and description "<description>"
        Examples:
            | id | title | completedStatus | activeStatus | description |
            | 1 | Office Work Updated | True | False | Office |
            | 1 | Home Work | False | False | Home |

    #Alternate Flow
    Scenario Outline: Update a project's fields to empty
        Given a project with id "<id>" exists
        When a user initiates the update of the project with id "<id>" to title "<title>", completed status "<completedStatus>", active status "<activeStatus>", and description "<description>"
        Then the project with id "<id>" will have title "<title>", completed status "<completedStatus>", active status "<activeStatus>", and description "<description>"
        Examples:
            | id | title | completedStatus | activeStatus | description |
            | 1 |  | True | False | Office |
            | 1 | Home Work | False | False |  |
    
    
    #Error Flow
    Scenario Outline: Update a project that does not exist
        Given a project with id "<id>" does not exist
        When a user initiates the update of the project with id "<id>" to title "<title>", completed status "<completedStatus>", active status "<activeStatus>", and description "<description>"
        Then the project with id "<id>" will not exist
        Examples:
            | id | title | completedStatus | activeStatus | description |
            | 10000 | Office Work Updated | True | False | Office |
            | 50000 | Home Work | False | False | Home |
