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
  Scenario Outline:Attempting to delete a category by providing the incorrect id or no id
    Given there is no existent category with <incorrectId> in the system
    When  a user elects to delete a category by providing the category <incorrectId>, or leaving the field blank
    Then no cateogry will be removed from the system
    Examples:
      |incorrectId|
      |90909099090|
      |""         |

 
