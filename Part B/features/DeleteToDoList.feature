Feature: Delete a Todo
  As a user, I want to delete a todo, so that it no longer exists in the system

  #Normal Flow
  Scenario Outline: Delete a todo
    Given existing todos in the system with <title>, <doneStatus>, <description>
    When a user elects to delete a todo by correctly providing the todo id
    Then the todo with the provided id will be removed from the system
    Examples:
      | title                        | doneStatus | description |
      | ECSE429 registration         | False      | register for class and tutorial sections |
      | ECSE429 find a project group | False      | post on discussion board to find teammates |

    #Error Flow
  Scenario Outline: Attempting to delete a todo by providing the incorrect id
    Given existing todos in the system with <title>, <doneStatus>, <description>
    And there is no existent todo with <incorrectId> in the system
    When a user elects to delete a todo by providing the <incorrectId>
    Then no todo will be removed from the system, and an error message is returned
    Examples:
      | title                        | doneStatus | description                                | incorrectId |
      | ECSE429 registration         | False      | register for class and tutorial sections   | 90909099090 |
      | ECSE429 find a project group | False      | post on discussion board to find teammates | 20000000000 |

    #Alternate Flow
  Scenario Outline: Attempting to delete a category by providing the no id
    Given existing todos in the system with <title>, <doneStatus>, <description>
    When a user elects to delete a todo, but does not specify a todo id
    Then no todo will be removed from the system, a "404 Not Found" Error occurs, and the return statement is blank
    Examples:
      | title                        | doneStatus | description                                |
      | ECSE429 registration         | False      | register for class and tutorial sections   |
      | ECSE429 find a project group | False      | post on discussion board to find teammates |


