Feature: Fetch all Todos Relating to a Category

  As a user, I want to fetch all the todos items related to a category, so that I can see how often the category is used

  #Normal Flow
  Scenario Outline: Fetch all todo items related to a category
    Given a todo with <title>, <description>, <doneStatus> and at least one category exist in the system with an existing relationship to category with id <categoryId>
    When a user fetches the todo items of a category by providing the category id <categoryId>
    Then the system will return all todos relating to the category, as well as the corresponding id, <description>, <title>, <doneStatus>, <taskOf>, and <categoryId> associated with the todos
    Examples:
      |title           |description                                   |doneStatus|taskOf   |categoryId|
      |Registration    |relating to registering for courses           |FALSE     |1        |1         |
      |Project Planning|relating to planning and logistics of projects|TRUE      |2        |2         |

#  Error Flow http://localhost:4567/categories/:id/todos
  Scenario Outline: Attempting to fetch all todos without providing a specific category id
    Given a todo with <title>, <description>, <doneStatus> and at least one category exist in the system with an existing relationship to category with id <categoryId>
    When a user fetches the todos of a category without specifying the category id
    Then the system will return all todos in the system that have relationships with any category and their corresponding id, <description>, <title>, <doneStatus>, <taskOf>, and <categoryId> associated with the todos
    Examples:
      |title           |description                                   |doneStatus|taskOf   |categoryId|
      |Registration    |relating to registering for courses           |FALSE     |1        |1         |
      |Project Planning|relating to planning and logistics of projects|TRUE      |2        |2         |


  #Error Flow http://localhost:4567/categories/THISISNOTANID/todos
  Scenario Outline: Attempting to fetch all todos relating to a category by providing an incorrect category id
    Given there are no categories with <incorrectId> in the system
    When a user elects to fetch all todos related to a category by providing the category <incorrectId>
    Then the system will return all todos in the system that have relationships with any category and their corresponding id, <description>, <title>, <doneStatus>, <taskOf>, and <categoryId> associated with the todos
    Examples:
      |title           |description                                   |doneStatus|taskOf   |categoryId|incorrectId|
      |Registration    |relating to registering for courses           |FALSE     |1        |1         |90909090900|
      |Project Planning|relating to planning and logistics of projects|TRUE      |2        |2         |2032938r982|

