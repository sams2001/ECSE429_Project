Feature: Fetch Categories by Project

  As a user, I want to fetch all categories related to a project, so I can view the categories relating to a project and their corresponding information

  #Normal Flow
  Scenario Outline: Fetch all categories via project
    Given their is at least one project in the system
    When a user fetches the categories via providing the project id
    Then the system will return all categories relating to the project, as well as the corresponding id, <description>, and <title>
    Examples:
      |description|title |
      |logistics  |title1|
      |accounting |title2|

  #Error Flow #http://localhost:4567/projects/:id/categories
  Scenario Outline: Attempting to fetch categories without providing a specific category id
    Given their is at least one project in the system
    When a user fetches the categories of a project without specifying the project id
    Then the system will return all categories in the system that have relationships with any project as well as the corresponding id, <description>, and <title>
    Examples:
      |description|title |
      |logistics  |title1|
      |accounting |title2|


  #Error Flow http://localhost:4567/projects/THISISNOTANID/categories
  Scenario Outline: Attempting to fetch categories by providing an id that does not exist
    Given there are no projects with <incorrectId> in the system
    When a user elects to fetch all categories related to a project by providing the <incorrectId>
    Then the system will return all categories in the system that have relationships with any project as well as the corresponding id, <description>, and <title>
    Examples:
      |description|title |
      |logistics  |title1|
      |accounting |title2|
