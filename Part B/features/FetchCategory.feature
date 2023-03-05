Feature: Fetch a Category

  As a user, I want to fetch a category, so that I can view all of the information corresponding to the category

  #Normal Flow
  Scenario Outline: Fetch and retrieve category
    Given existing categories in the system
    When a user fetches a category by providing the category id
    Then the system will return the category and its corresponding id, <description>, and <title>
    Examples:
      |title           |description                                   |
      |Registration    |relating to registering for courses           |

  #Alternate Flow
  Scenario: Fetch a specific category without providing an id
    Given existing categories in the system
    When a user fetches all categories
    Then all categories in the system will be returned

  #Error flow
  Scenario Outline: Attempting to fetch a category by using an id that does not exist
    Given there are no categories with <incorrectId> in the system
    When a user elects to fetch a category by providing the <incorrectId>
    Then an error message is returned containing the <incorrectId>
    Examples:
      |incorrectId|
      |90909099090|
      |99999      |
