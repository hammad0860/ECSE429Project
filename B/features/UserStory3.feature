Feature: Removing a TODO
  As a student, I want to remove a TODO, so that I can clear out tasks that are no longer needed.

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

Scenario Outline: Remove an existing TODO (Normal Flow)
  When the student deletes the TODO with title "<todo_title>"
  Then the TODO with the title "<todo_title>" should no longer exist
  And the student is notified that the removal operation was successful

  Examples:
    | todo_title               |
    | Implement a linked list  |
    | Analyze time complexity  |
    | Summarize Hamlet         |
    | Think about stuff        |

Scenario Outline: Remove a TODO that is associated with a project (Alternate Flow)
  Given the TODO "<todo_title>" is associated with the project "<project_title>"
  When the student deletes the TODO with title "<todo_title>"
  Then the TODO with the title "<todo_title>" should no longer exist
  And the student is notified that the removal operation was successful

  Examples:
    | todo_title              | project_title      |
    | Implement a linked list | Computer Science   |
    | Summarize Hamlet        | English Literature |

Scenario Outline: Attempting to remove a non-existent TODO (Error Flow)
  Given no TODO exists with the id "<id>"
  When the student deletes the TODO with id "<id>"
  Then the system should notify the student with the not found error message "<message>"

  Examples:
    | id  | message                                                |
    | 99  | Could not find any instances with todos/99             |
    | 100 | Could not find any instances with todos/100            |
