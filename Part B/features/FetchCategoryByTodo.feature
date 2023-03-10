Feature: Fetch Category or Categories via Todo

  As a user, I want to fetch a category by a todo, so that I can view the categories and their information corresponding to a todo

  #Normal Flow
  Scenario Outline: Fetch category via todo
    Given that category with id <categoryid> exists in the system
    And that todo with id <todoid> exists in the system 
    And that todo with id <todoid> has a relationship to the category with id <categoryid>
    When fetching categories via todo <todoid>
    Then the category <categoryid> associated with todo <todoid> shall be returned
    Examples:
        |todoid|categoryid|
        |1|1|
        |3|2|


  #Alternate Flow
  Scenario Outline: Fetch categories via todo
    Given that categories with ids <categoryid> exists in the system
    And that todo with id <todoid> exists in the system 
    And that todo with id <todoid> has a relationship to the categories with ids <categoryid>
    When fetching categories via todo <todoid>
    Then all of the categories <categoryid> associated with todo <todoid> shall be returned
    Examples:
        |todoid|categoryid|
        |1|1,2|
        |3|1,2,3|


  #Error flow
  Scenario Outline: Fetch category via todo that does not exist
    Given that category with id <categoryid> exists in the system
    And that todo with id <todoid> does not exist in the system 
    When fetching categories via todo <todoid>
    Then will return an error message
    Examples:
        |todoid|categoryid|
        |1000|1|
        |30000|2|
