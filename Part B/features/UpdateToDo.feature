Feature: Update a Todo

  As a user, I want to update a todo, so I can reflect the progress that I've made on the project

  #Normal Flow
  Scenario Outline: Update a Todo
    Given at least one todo exists in the system
    When a user updates a todo by providing the todo id and updated <title>, <description>, <doneStatus>, and <taskOf>
    Then the system will append the changed fields and return the todo and its corresponding id, <title>, <description>, <doneStatus>, and <taskOf>
    Examples:
      |title           |description                                   |doneStatus|taskOf   |
      |Registration    |relating to registering for courses           |False     |1|
      |Project Planning|relating to planning and logistics of projects|True      |1|

  #Alternate Flow
  Scenario Outline: Updating a todo without providing all fields
    Given at least one todo exists in the system
    When a user updates a todo by only providing the todo id and updated <title>
    Then the system will append the changed <title> and return the todo and its corresponding information, the description will be set to an empty string, the doneStatus will be set to false, the taskOf relationship will be voided
    Examples:
      |title           |
      |Registration    |
      |Project Planning|


  #Error flow
  Scenario Outline: Attempting to update a todo by using an id that does not exist
    Given there are no todos with <incorrectId> in the system
    When a user elects to update a todo by providing the <incorrectId>
    Then an error message is returned
    Examples:
      |incorrectId|
      |90909099090|
      |99999      |
