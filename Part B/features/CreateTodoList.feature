Feature: Create a todo list for classes

  As a user, I want to create a to do item, so that I can track a list of tasks to complete

  #Normal Flow
  Scenario Outline: Create a todo item
    Given the project is running
    When a user creates a new todo item with <title>, <doneStatus>, <description>
    Then a new todo item is created with <title>, <doneStatus>, <description>
    Examples:
      | title | doneStatus | description |
      | ECSE429 registration | False | register for class and tutorial sections |
      | ECSE429 find a project group | False | post on discussion board to find teammates |


  #Error flow
  Scenario Outline: Create a todo item with incorrect payload
    Given the project is running
    When a user attempts to create a new todo item with <title>, <doneStatus>, <description>, <id>
    Then no new item is created
    Examples:
      | title | doneStatus | description | id |
      | ECSE429 registration | False | register for class and tutorial sections | 100000 |