Feature: Delete a Category

  As a user, I want to delete a category, so that it no longer exists in the system

  #Normal Flow
  Scenario Outline: Delete a category
    Given a category with <id> exists in the system
    When a user elects to delete a category by correctly providing the category <id>
    Then the category with <id> will be removed from the system
    Examples:
      |id|
      |65|
      |2 |

  #Error Flow
  Scenario Outline:Attempting to delete a category by providing the incorrect id
    Given there is no existent category with <incorrectId> in the system
    When  a user elects to delete a category by providing the <incorrectId>
    Then no category will be removed from the system, and an error message "Could not find any instances with categories/" + "<incorrectId>" is returned
    Examples:
      |incorrectId|
      |90909099090|
      |""         |
     #Error Flow
  Scenario: Attempting to delete a category by providing the no id
    Given there are existent categories in the system
    When  a user elects to delete a category, but does not specify a category id
    Then no project will be removed from the system, a "404 Not Found" Error occurs, and the return statement is blank


