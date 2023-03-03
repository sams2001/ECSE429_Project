Feature: Create a Category

  As a user, I want to create a category, so that I can relate my similar todo items to a category

  #Normal Flow
  Scenario Outline: Create a category
    Given the project is running
    When a user creates a new category with a <title> and <description>
    Then a new category is created with <title>, <description> and an auto-generated id
    Examples:
      |title           |description                                   |
      |Registration    |relating to registering for courses           |
      |Project Planning|relating to planning and logistics of projects|

  #Alternate Flow
  Scenario Outline:Create a category with a null description
    Given the project is running
    When a user creates a new category by providing a valid <title>, and leaves the description blank
    Then a new category is created with <title>, a null description, and an auto-generated id
    Examples:
    |title                |
    |void Description     |
    |Forgotten Description|

  #Error flow
  Scenario Outline: Attempting to create a category without providing a title, or an empty string as the title
    Given the project is running
    When a user attempts to create a new category but provides a <blankTitle>, and a valid <description>
    Then no new item is created, and an error message "title : field is mandatory" is returned
    Examples:
      | blankTitle | description|
      | ""    |not sure what this will be so I'll leave the title blank for now|
      |    "" |hmmm... lets see what happens if I leave my title blank         |

#for this error flow, the syntax of having an empty string is probably wrong once I get into the step definitions