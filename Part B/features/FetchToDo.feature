Feature: Fetch a Todo

  As a user, I want to fetch a todo, so that I can view all of the information corresponding to the todo

  #Normal Flow
  Scenario Outline: Fetch and retrieve todo
    Given todos exist in the system
    When a user fetches a todo by providing the todo id
    Then the system will return the todo and its corresponding id, <description>, <title>, <doneStatus>, <taskOf>, and <categories> associated with the todo
    Examples:
      |title              |description                                   |doneStatus|taskOf   |categories|
      |Register for course|register for MECH261                          |FALSE     |1        | 1        |

  #Alternate Flow
  Scenario Outline: Attempting to fetch a specific todo without providing an id
    Given at least one todo exists in the system
    When a user fetches a todo without providing the specific id of the todo
    Then the system will return all todos in the system and their corresponding id, <description>, <title>, <doneStatus>, <taskOf>, and <categories> associated with the todos
    Examples:
      |title              |description                                   |doneStatus|taskOf   |categories|
      |Register for course|register for MECH261                          |FALSE     |1        |1         |
      |Plan project       |create project team                           |TRUE      |2        |     2    |


  #Error flow
  Scenario Outline: Attempting to fetch a todo by using an id that does not exist
    Given there are no todos with <incorrectId> in the system
    When a user elects to fetch a todos by providing the <incorrectId>
    Then an error message is returned containing the <incorrectId>
    Examples:
      |incorrectId|
      |90909099090|
      |99999      |
