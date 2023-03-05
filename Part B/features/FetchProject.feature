Feature: Fetch a Project

  As a user, I want to fetch a project, so that I can view all of the information corresponding to the project

  #Normal Flow
  Scenario Outline: Fetch and retrieve project
    Given a project exists in the system with id <id>
    When a user fetches a project by providing the project id <id>
    Then the system will return the project and its corresponding <id>, and related feilds
    Examples:
      |id|
      |1 |
      |2 |

  #Alternate Flow
  Scenario Outline: Attempting to fetch project(s) without providing an id
    Given at least one project exists in the system
    When a user fetches project(s) without providing a specific project id
    Then all projects in the system and their corresponding id, and related feilds are returned

  #Error flow
  Scenario Outline: Attempting to fetch a project by using an id that does not exist
    Given there are no projects with <incorrectId> in the system
    When a user fetches a project by providing the project id <incorrectId>
    Then a 404 Not Found Error occurs, and the return statement is blank

    Examples:
      |incorrectId|
      |90909099090|
      |99999      |
