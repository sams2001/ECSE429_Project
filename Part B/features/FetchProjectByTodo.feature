Feature: Fetch Project or Projects via Todo

  As a user, I want to fetch project(s) related to a task, so that I can view the information of a project corresponding to a task.

  #Normal Flow: GET /todos/:id/tasksof
  Scenario Outline: Fetch project by a todo
    Given that todo with id <taskid> exists in the system 
    Given a project with id <projectid> exists with related tasks <taskid>
    When a user fetches projects via task id <taskid>
    Then the project <projectid> related to task <taskid> shall be returned
    Examples:
        |projectid|taskid|
        |1|1|
        |2|3|

   #Alternate Flow: 
   Scenario Outline: Fetch project by a todo with no related projects
    Given todo with id <taskid> exists in the system with no related projects
    When a user fetches projects via task id <taskid>
    Then an empty list of projects related to task <taskid> shall be returned
    Examples:
        |taskid|
        |1|
        |3|

   #Alternate Flow: 
   Scenario Outline: Fetch project by a todo with no related projects
    Given todo with id <taskid> does not exist
    Then an error message shall be returned when a user fetches projects via task id <taskid>
    Examples:
        |taskid|
        |17|
        |3|