Feature: Fetch a Project

  As a user, I want to fetch a project, so that I can view all of the information corresponding to the project

  #Normal Flow
  Scenario Outline: Fetch and retrieve project
    Given at least one project exists in the system
    When a user fetches a project by providing the project id
    Then the system will return the project and its corresponding id, <title>, <description>, <completed> status, <active> status, and <tasks> is returned
    Examples:
      |title           |description                                   |completed|active|tasks|
      |Big Proj 1      |relating to registering for courses           |FALSE    |TRUE  |"id":"1"|
      |MegaProject 5   |relating to planning and logistics of projects|FALSE    |FALSE |"id":"2"|

  #Alternate Flow
  Scenario Outline: Attempting to fetch project(s) without providing an id
    Given at least one project exists in the system
    When a user fetches project(s) without providing a specific project id
    Then all projects in the system and their corresponding id, <title>, <description>, <completed> status, <active> status, and <tasks> are returned
    Examples:
      |title           |description                                   |completed|active|tasks|
      |Big Proj 1      |relating to registering for courses           |FALSE    |TRUE  |"id":"1"|
      |MegaProject 5   |relating to planning and logistics of projects|FALSE    |FALSE |"id":"2"|

  #Error flow
  Scenario Outline: Attempting to fetch a project by using an id that does not exist
    Given there are no projects with <incorrectId> in the system
    When a user elects to fetch a category by providing the <incorrectId>
    Then a "404 Not Found" Error occurs, and the return statement is blank

    Examples:
      |incorrectId|
      |90909099090|
      |99999      |
