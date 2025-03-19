Feature: Associating a TODO with a Project
  As a student, I want to associate a TODO with a project, so that I can keep related tasks grouped together.

Background:
  Given the server is running
  And the following TODOS exist:
    | todo_title               | doneStatus | description                     |
    | Implement a linked list  | false      | data structure assignment       |
    | Analyze time complexity  | false      | O(n) vs O(log n) analysis       |
    | Summarize Hamlet         | false      | Focus on Act 3                  |
    | Think about stuff        | false      | dont think too much             |
  And the following PROJECTS exist:
    | project_title       | completed | description                          | active |
    | Computer Science    | false     | Data Structures and Algorithms       | true   |
    | ECSE 202            | false     | Intro to Software English            | true   |
    | English Literature  | false     | Study of Shakespearean Sonnets       | true   |
    | Philosophy 201      | false     | Survey of Ancient Philosophers       | true   |

Scenario Outline: Associate a TODO with a Project (Normal Flow)
  When the student associates the TODO "<todo_title>" with the project "<project_title>"
  Then the TODO "<todo_title>" should be associated with the project "<project_title>"
  And the student is notified that the association operation was successful

  Examples:
    | todo_title              | project_title       |
    | Implement a linked list | Computer Science    |
    | Summarize Hamlet        | English Literature  |

Scenario Outline: Change a TODO's association to a different project (Alternate Flow)
  Given the TODO "<todo_title>" is associated with the project "<original_project>"
  When the student associates the TODO "<todo_title>" with a different project "<new_project>"
  Then the TODO "<todo_title>" should be associated with both projects "<original_project>" and "<new_project>"
  And the student is notified that the association operation was successful

  Examples:
    | todo_title               | original_project    | new_project         |
    | Implement a linked list  | Computer Science    | ECSE 202            |
    | Analyze time complexity  | ECSE 202            | Computer Science    |
    | Summarize Hamlet         | English Literature  | Philosophy 201      |
    | Think about stuff        | Philosophy 201      | English Literature  |

Scenario Outline: Attempt to Associate a Non-existent TODO with a Project (Error Flow)
  Given no TODO exists with the id "<id>"
  When the student attempts to associate the TODO with id "<id>" with the project "<project_title>"
  Then the system should notify the student with the not found error message "<message>"

  Examples:
    | id  | project_title    | message                                                                 |
    | 99  | Philosophy 201   | Could not find parent thing for relationship todos/99/tasksof           |
