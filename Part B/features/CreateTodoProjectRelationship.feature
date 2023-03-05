Feature: Create relationship between project and todo

  As a user, I want to create a relationship between a project and todo, so that I can better and more dynamically organize my todos.

  Background:
    Given the application is running

  #Normal Flow: POST /projects/:id/tasks
  Scenario Outline: Create relationship between existing project and existing todo via /projects
    Given todo with id <todoid> exists in the system with no relationship to project <projectid>
    Given a project with id <projectid> exists in the system
    When a user creates a relationship between todo <todoid> and project <projectid> on the project side
    Then the todo <todoid> will be related to project <projectid>
    Then the project <projectid> will be related to todo <todoid>
    Examples:
        |projectid|todoid|
        |1|3|
        |2|1,2|

  #Alternate Flow: POST /todos/:id/tasksof
  Scenario Outline: Create relationship between existing project and existing todo via /todos
    Given todo with id <todoid> exists in the system with no relationship to project <projectid>
    Given a project with id <projectid> exists in the system
    When a user creates a relationship between todo <todoid> and project <projectid> on the todos side
    Then the todo <todoid> will be related to project <projectid>
    Then the project <projectid> will be related to todo <todoid>
    Examples:
        |projectid|todoid|
        |1|3|
        |2|1,2|

  #Error flow
  Scenario Outline: Create relationship between non-existing project and existing todo via /todos
    Given todo with id <todoid> exists in the system with no relationship to project <projectid>
    Given a project with id <projectid> does not exist
    When a user creates a relationship between todo <todoid> and project <projectid> on the todos side
    Then the todo <todoid> will not be related to project <projectid>
    Then the project <projectid> will not be related to todo <todoid>
    Examples:
        |projectid|todoid|
        |100|3|
        |23|1,2|

  #Error flow
  Scenario Outline: Create relationship between non-existing project and existing todo via /projects
    Given todo with id <todoid> exists in the system with no relationship to project <projectid>
    Given a project with id <projectid> does not exist
    When a user creates a relationship between todo <todoid> and project <projectid> on the project side
    Then the todo <todoid> will not be related to project <projectid>
    Then the project <projectid> will not be related to todo <todoid>
    Examples:
        |projectid|todoid|
        |100|3|
        |23|1,2|