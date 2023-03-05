Feature: Create a Project

  As a user, I want to create a project, so I can organize todos and tasks inside the project

  #Normal Flow
  Scenario Outline: Create a project
    Given the project is running
    When a user creates a new project with a <title>, <description>, <completed> status, and <active> status
    Then a new project is created with <title>, <description>, <completed> status, <active> status, and an auto-generated id
    Examples:
      |title           |description               |completed|active|
      |Diet Plan       |Dieting plan and logistics|TRUE     |FALSE |
      |API Testing     |Part B of API testing     |FALSE    |TRUE  |

  #Error Flow EX:http://localhost:4567/projects/56
  Scenario Outline:
    Given the project is running
    When a user attempts to create a new project by providing an <unnecessaryId> in the call statement
    Then no new project will be created, and an error with the error message "No such project entity instance with GUID or ID <unnecessaryId> found" will be returned
    Examples:
    |unnecessaryId|
    |56           |
    |57           |
  #Alternate Flow
  Scenario: Create a project with blank fields
    Given the project is running
    When  a user creates a new project without entering information into any of the fields
    Then a new project is created with an auto-generated id, a false completed status, a false active status, and all other fields blank



