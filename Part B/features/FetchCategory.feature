Feature: Create a Category

  As a user, I want to fetch a category, so that I can view all of the information corresponding to the category

  #Normal Flow
  Scenario Outline: Fetch and retrieve category
    Given a category with <id> exists in the system
    When a user fetches a category by providing the category <id>
    Then the system will return the category and its corresponding <id>, <description>, and <title>
    Examples:
      |title           |description                                   |id|
      |Registration    |relating to registering for courses           |65|
      |Project Planning|relating to planning and logistics of projects|2 |

  #Alternate Flow
  Scenario Outline: Attempting to fetch a specific category without providing an id
    Given at least one category exists in the system
    When a user fetches a category without providing the specific id of the category
    Then all categories in the system and their corresponding <id>, <description>, and <title> will be returned
    Examples:
      |title           |description                                   |id|
      |Registration    |relating to registering for courses           |65|
      |Project Planning|relating to planning and logistics of projects|2 |

  #Error flow
  Scenario Outline: Attempting to fetch a category by using an id that does not exist
    Given there are no categories with <incorrectId> in the system
    When a user elects to fetch a category by providing the <incorrectId>
    Then an error message "Could not find any instances with categories/" + "<incorrectId>" is returned
    Examples:
      |incorrectId|
      |90909099090|
      |99999      |
