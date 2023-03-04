Feature: Fetch a Todo

  As a user, I want to fetch a todo, so that I can view all of the information corresponding to the todo

  #Normal Flow
  Scenario Outline: Fetch and retrieve todo
    Given at least one todo exists in the system
    When a user fetches a todo by providing the todo id
    Then the system will return the todo and its corresponding id, <description>, <title>, <doneStatus>, <taskOf>, and <categories> associated with the todo
    Examples:
      |title           |description                                   |title |doneStatus|taskOf   |categories|
      |Registration    |relating to registering for courses           |title1|FALSE     |"id": "1"|"id": "1" |
      |Project Planning|relating to planning and logistics of projects|title2|TRUE      |"id": "2"|"id": "2" |

  #Alternate Flow
  Scenario Outline: Attempting to fetch a specific todo without providing an id
    Given at least one todo exists in the system
    When a user fetches a todo without providing the specific id of the todo
    Then the system will return all todos in the system and their corresponding id, <description>, <title>, <doneStatus>, <taskOf>, and <categories> associated with the todos
    Examples:
      |title           |description                                   |title |doneStatus|taskOf   |categories|
      |Registration    |relating to registering for courses           |title1|FALSE     |"id": "1"|"id": "1" |
      |Project Planning|relating to planning and logistics of projects|title2|TRUE      |"id": "2"|"id": "2" |


  #Error flow
  Scenario Outline: Attempting to fetch a todo by using an id that does not exist
    Given there are no todos with <incorrectId> in the system
    When a user elects to fetch a todos by providing the <incorrectId>
    Then an error message "Could not find any instances with todos/" + "<incorrectId>" is returned
    Examples:
      |incorrectId|
      |90909099090|
      |99999      |
