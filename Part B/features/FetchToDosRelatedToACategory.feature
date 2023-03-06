Feature: Fetch all Todos Relating to a Category

  As a user, I want to fetch all the todos items related to a category, so that I can see how often the category is used

  #Normal Flow
  Scenario Outline: Fetch all todo items related to one category
    Given a todo with <title>, <description>, <doneStatus> and one category exist in the system with an existing relationship to category with id <categoryId>
    When a user fetches the todo items of a category by providing the category id <categoryId>
    Then the system will return the todo related to the category, as well as the corresponding id, <description>, <title>, <doneStatus>, and <categoryId> associated with the todos
    Examples:
      |title           |description                                   |doneStatus|categoryId|
      |Registration    |relating to registering for courses           |FALSE     |1         |
      |Project Planning|relating to planning and logistics of projects|TRUE      |2         |

#  Alternate flow
  Scenario Outline: Fetch multiple todo items related to one category
    Given todo items with <title>, <description>, <doneStatus>, <title2>, <description2>, <doneStatus2> and one category exist in the system with an existing relationship to a category with id '1'
    When a user fetches the todo items of both categories
    Then the system will return all todos relating both categories, as well as the corresponding id, <description>, <title>, <doneStatus>, associated with the todos
    Examples:
      |title           |description                                   |doneStatus| title2 | description2 | doneStatus2 |
      |Registration    |relating to registering for courses           |FALSE     | example| example desc | TRUE        |
      |Project Planning|relating to planning and logistics of projects|TRUE      | test   | jnkac        |False        |


  #Error Flow
  Scenario Outline: Attempting to fetch all todos relating to a category by providing an incorrect category id
    Given there are no categories with <incorrectId> in the system
    When a user elects to fetch all todos related to a category by providing the category <incorrectId>
    Then the system will return all todos in the system that have relationships with any category and their corresponding id, <description>, <title>, <doneStatus>, and <categoryId> associated with the todos
    Examples:
      |title           |description                                   |doneStatus| categoryId|incorrectId|
      |Registration    |relating to registering for courses           |FALSE     |1          |90909090900|
      |Project Planning|relating to planning and logistics of projects|TRUE      |2          |2032938r982|

