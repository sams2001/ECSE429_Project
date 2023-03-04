Feature: Update a Todo

  As a user, I want to update a todo, so I can reflect the progress that I've made on the project

  #Normal Flow
  Scenario Outline: Update a Todo
    Given at least one todo exists in the system
    When a user updates a todo by providing the todo id and updated <description>, <title>, <doneStatus>, <taskOf>, and <categories> associated
    Then the system will append the changed fields and return the todo and its corresponding id, <description>, <title>, <doneStatus>, <taskOf>, and <categories> associated with the todo
    Examples:
      |title           |description                                   |title |doneStatus|taskOf   |categories|
      |Registration    |relating to registering for courses           |title1|FALSE     |"id": "1"|"id": "1" |
      |Project Planning|relating to planning and logistics of projects|title2|TRUE      |"id": "2"|"id": "2" |

  #Alternate Flow
  Scenario Outline: Updating a todo without providing all fields
    Given at least one todo exists in the system
    When a user updates a todo by providing the todo id and updated <title>
    Then the system will append the changed <title> and return the todo and its corresponding information, the description will be set to an empty string, the doneStatus will be set to false, the task and category relationships will be voided
    Examples:
      |title           |title |
      |Registration    |title1|
      |Project Planning|title2|


  #Error flow
  Scenario Outline: Attempting to update a todo by using an id that does not exist
    Given there are no todos with <incorrectId> in the system
    When a user elects to update a todo by providing the <incorrectId>
    Then an error message "Invalid GUID for" + "<incorrectId>" + "entity todo"" is returned
    Examples:
      |incorrectId|
      |90909099090|
      |99999      |
