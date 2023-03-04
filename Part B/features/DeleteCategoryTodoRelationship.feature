Feature: Delete relationship between category and todo

    As a user, I want to delete a relationship between a todo and category, so that I can better and more dynamically organize my todos.

    Background:
        Given the application is running

    #Normal flow: DELETE /todos/:id/categories/:id
    Scenario Outline: Deleting a relationship between an existing todo and category via todos
    Given that category with id <categoryid> exists in the system
    And that todo with id <todoid> exists in the system 
    And that todo with id <todoid> has a relationship to the category with id <categoryid>
    When a relationship between todo <todoid> and category <categoryid> is deleted on the todos side
    Then todo <todoid> will not have a relation to category <categoryid>
    Then category <categoryid> will not have a relation to todo <todoid>
    Examples:
      |categoryid |todoid |
      |1|1|
      |3|2|

    #Alternate flow: DELETE /categories/:id/todos/:id
    Scenario Outline: Deleting a relationship between an existing todo and category via categories
    Given that category with id <categoryid> exists in the system
    And that todo with id <todoid> exists in the system 
    And that todo with id <todoid> has a relationship to the category with id <categoryid>
    When a relationship between todo <todoid> and category <categoryid> is deleted on the categories side
    Then todo <todoid> will not have a relation to category <categoryid>
    Then category <categoryid> will not have a relation to todo <todoid>
    Examples:
      |categoryid |todoid |
      |1|1|
      |3|2|

    #Alternate flow
    Scenario Outline: Deleting a relationship between a todo and category that doesn't exist
    Given that category with id <categoryid> exists in the system
    And that todo with id <todoid> exists in the system 
    And that todo with id <todoid> has no relationship to the category with id <categoryid>
    When a relationship between todo <todoid> and category <categoryid> is deleted on the todos side
    Then todo <todoid> will not have a relation to category <categoryid>
    Then category <categoryid> will not have a relation to todo <todoid>
    Examples:
      |categoryid |todoid |
      |1|1|
      |3|2|

    #Error flow
    Scenario Outline: Deleting a relationship between a non-existing todo and category that doesn't exist
    Given that category with id <categoryid> exists in the system
    And that todo with id <todoid> does not exist in the system 
    Then an error will be raised when a relationship between todo <todoid> and category <categoryid> is deleted on the todos side
    Examples:
      |categoryid |todoid |
      |1|1000|
      |3|2000|


    