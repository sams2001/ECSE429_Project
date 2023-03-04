Feature: Create relationship between category and todo

    As a user, I want to create a relationship between a todo and category, so that I can better organize my todos.

    Background:
        Given the application is running

    #Normal flow
    Scenario Outline: Adding a relationship between an existing todo and category
    Given that category with id <categoryid> exists in the system
    And that todo with id <todoid> exists in the system 
    And that todo with id <todoid> has no relationship to the category with <categoryid>
    When a relationship between todo <todoid> and category <categoryid> is instantiated
    Then todo <todoid> will have a relation to category <categoryid>
    Examples:
      |categoryid |todoid |
      |1|1|
      |3|2|

    #Alternate flow
    Scenario Outline: Adding a relationship between a todo and category on creation of the todo
    Given that category with id <categoryid> exists in the system
    When a new todo is created with a relationship to category <categoryid>
    Then the new todo will have a relation to category <categoryid>
    Examples:
      |categoryid |
      |1|
      |3|

    #Error flow
    Scenario Outline: Adding a relationship between an existing todo and non-existing category
    Given that category with id <categoryid> exists in the system
    When a new todo is created with a relationship to category <categoryid>
    Then the new todo will not have a relation to category <categoryid>
    Examples:
      |categoryid |
      |1 |
      |3 |