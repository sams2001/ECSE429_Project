Feature: Delete a Todo
  As a user, I want to delete a todo, so that it no longer exists in the system

  Scenario: Delete a todo
    Given at least one todo exists in the system
    When a user elects to delete a todo by correctly providing the todo id
    Then the todo with the provided id will be removed from the system

  Scenario Outline: Attempting to delete a todo by providing the incorrect id
    Given there is no existent todo with <incorrectId> in the system
    When a user elects to delete a todo by providing the <incorrectId>
    Then no todo will be removed from the system, and an error message is returned

    Examples:
      | incorrectId |
      | 90909099090 |
      | 20000000000 |

  Scenario: Attempting to delete a category by providing the no id
    Given there are existent todos in the system
    When a user elects to delete a todo, but does not specify a todo id
    Then no todo will be removed from the system, a "404 Not Found" Error occurs, and the return statement is blank



