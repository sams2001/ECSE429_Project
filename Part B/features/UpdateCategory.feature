Feature: Update a pre-existing category's field/s

    As a user, I want to update a category's fields, so that I do not have to delete and create a new category.


    Background:
        Given the application is running

    #Normal Flow
    Scenario Outline: Update a category's name and description
        Given a category with id '1' exists
        When a user initiates the update of the category with id '1' to title "<title>" and description "<description>"
        Then the category with id '1' will have title "<title>" and description "<description>"
        Examples:
            | id | title | description |
            | 1 | Office Updated | Office work. |
            | 1 | Office Updated | Tgkjdnlskfd |
    
    
    #Alternate Flow
    Scenario Outline: Update a category to empty
        Given a category with id '1' exists
        When a user initiates the update of the category with id '1' to title "<title>" and description "<description>"
        Then the category with id '1' will have title "<title>" and description "<description>"
        Examples:
            | id | title | description |
            | 1 |  | Office work. |
            | 1 | Office Updated |  |
    
    
    #Error Flow
    Scenario Outline: Update a category that does not exist
        Given a category with id '10000' does not exist
        When a user initiates the update of the category with id '10000' to title "<title>" and description "<description>"
        Then the category with id '10000' will not exist
        Examples:
            | id | title | description |
            | 1 | Office Updated | Office work. |
            | 1 | Office Updated | Tgkjdnlskfd |
