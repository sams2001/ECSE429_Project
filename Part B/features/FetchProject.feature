Feature: Fetch a Project

  As a user, I want to fetch a project, so that I can view all of the information corresponding to the project

  #Normal Flow
  Scenario Outline: Fetch and retrieve project
    Given a project exists in the system with with a <title>, <description>, <completed> status, and <active> status
    When a user fetches a project by providing the project id
    Then the system will return the project and its corresponding and related fields
    Examples:
      | title       | description                | completed | active |
      | Diet Plan   | Dieting plan and logistics | TRUE      | FALSE  |
      | API Testing | Part B of API testing      | FALSE     | TRUE   |

  #Alternate Flow
  Scenario Outline: Attempting to fetch project(s) without providing an id
    Given a project exists in the system with with a <title>, <description>, <completed> status, and <active> status
    When a user fetches project(s) without providing a specific project id
    Then all projects in the system and their corresponding id, and related fields are returned
    Examples:
      | title       | description                | completed | active |
      | Diet Plan   | Dieting plan and logistics | TRUE      | FALSE  |
      | API Testing | Part B of API testing      | FALSE     | TRUE   |

  #Error flow
  Scenario Outline: Attempting to fetch a project by using an id that does not exist
    Given a project exists in the system with with a <title>, <description>, <completed> status, and <active> status
    And there are no projects with <incorrectId> in the system
    When a user fetches a project by providing the project id <incorrectId>
    Then a 404 Not Found Error occurs, and the return statement is blank

    Examples:
      | title       | description                | completed | active |incorrectId|
      | Diet Plan   | Dieting plan and logistics | TRUE      | FALSE  |90909099090|
      | API Testing | Part B of API testing      | FALSE     | TRUE   |99999      |
