Feature: Fetch Todo or Todos via Project

  As a user, I want to fetch todos by a project, so that I can view the tasks and their information corresponding to a project

  #Normal Flow:
  Scenario Outline: Fetch todo by a project
    Given todos with ids <taskids> exist in the system
    Given a project with id <projectid> exists with related tasks <taskids>
    When a user fetches tasks via project with project id <projectid>
    Then the tasks <taskids> related to project <projectid> shall be returned
    Examples:
        |projectid|taskids|
        |1|1,2|
        |2|2|

  #Alternate Flow: 
  Scenario Outline: Fetch todo by a project with no todos
    Given a project with id <projectid> exists with no related tasks
    When a user fetches tasks via project with project id <projectid>
    Then no tasks related to project <projectid> shall be returned
    Examples:
        |projectid|
        |4|

  #Error flow
  Scenario Outline: Fetch todo by a project with no todos
    Given a project with id <projectid> does not exist
    When a user fetches tasks via project with project id <projectid>
    Then an error message will be returned upon the request for project <projectid> tasks
    Examples:
        |projectid|
        |100|

