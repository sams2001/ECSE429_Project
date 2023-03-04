Feature: Create a todo list for classes

  As a user, I want to create a todo item, so that I can track a list of tasks to complete

  #Normal Flow
  Scenario Outline: Create a todo item
    Given the project is running
    When a user creates a new todo item with <title>, <doneStatus>, <description>
    Then a new todo item is created with <title>, <doneStatus>, <description>, and an auto-generated id
    Examples:
      | title                        | doneStatus | description |
      | ECSE429 registration         | False      | register for class and tutorial sections |
      | ECSE429 find a project group | False      | post on discussion board to find teammates |

 #Alternate Flow
  Scenario Outline: Create a todo with a title, but null fields
    Given the project is running
    When a user creates a new todo by providing a valid <title>, and leaves the description and done status blank
    Then a new category is created with <title>, a null description, a "false" done status, and an auto-generated id
    Examples:
      |title                |
      |void Description     |
      |Forgotten Description|
  #Error flow
  Scenario Outline: Attempting to create a todo without providing a title
    Given the project is running
    When a user attempts to create a new todo item with <title>, <doneStatus>, <description>, <id>
    Then no new item is created
    Examples:
      | title | doneStatus | description | id |
      | ECSE429 registration | False | register for class and tutorial sections | 100000 |