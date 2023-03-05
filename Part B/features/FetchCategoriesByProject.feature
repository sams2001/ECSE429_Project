Feature: Fetch Categories by Project

  As a user, I want to fetch all categories related to a project, so I can view the categories relating to a project and their corresponding information

  #Normal Flow
  Scenario Outline: Fetch all categories via project
    Given a category with id <catid> exist in the system
    Given a project with id <projectid> exists with related category <catid>
    When a user fetches the category via providing the project id <projectid>
    Then the system will return all categories relating to the project, as well as the corresponding id <catid>
    Examples:
      |catid|projectid|
      |1,2  |1        |
      |3    |2        |

  #Error Flow #http://localhost:4567/projects/:id/categories
  Scenario Outline: Attempting to fetch categories without providing a specific category id
    Given their is at least one project in the system with associated categories
    When a user fetches the categories of a project without specifying the project id
    Then the system will return all categories in the system that have relationships with any project as well as the corresponding id
    Examples:
      |catid|
      |1    |


  #Error Flow http://localhost:4567/projects/THISISNOTANID/categories
  Scenario Outline: Attempting to fetch categories by providing an id that does not exist
    Given there are no projects with <incorrectId> in the system
    When a user elects to fetch all categories related to a project by providing the <incorrectId>
    Then the system will return all categories in the system that have relationships with any project as well as the corresponding id
    Examples:
      |incorrectId|
      |9999909    |
