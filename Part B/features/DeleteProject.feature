Feature: Delete a Project

  As a user, I want to delete a project, so that it no longer exists in the system

  #Normal Flow
  Scenario: Delete a project
    Given project(s) exist in the system
    When a user elects to delete a project by correctly providing the project id
    Then the project with the provided id will be removed from the system

  #Error Flow
  Scenario Outline: Attempting to delete a project by providing the incorrect id
    Given there is no existent project with <incorrectId> in the system
    When  a user elects to delete a project by providing the <incorrectId>
    Then no project will be removed from the system, and an error message is returned
    Examples:
      |incorrectId|
      |20000000000|
      |90909090909|
  #Error Flow
  Scenario: Attempting to delete a project by providing no id
    Given project(s) exist in the system
    When  a user elects to delete a project, but does not specify a project id
    Then no project will be removed from the system, a "404 Not Found" Error occurs, and the return statement is blank
