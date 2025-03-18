Feature: Updating the Description of TODOS
  As a student, I want to change the description of a TODO, so that I can track the current information of my tasks more efficiently.

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


Scenario Outline: Change a TODO's description (Normal Flow)
  When the student updates the todo "<todo_title>" to have a new description "<new_description>"
  Then the todo "<todo_title>" should now have the description "<new_description>"
  And the student is notified that the update operation was successful

  Examples:
    | todo_title              | new_description                              |
    | Implement a linked list | Advanced Data Structures and Algorithms      |
    | Summarize Hamlet        | Elizabethan drama and poetry                 |
    | Analyze time complexity | Analyze space complexity                     |
    | Think about stuff       | Survey of Ancient Philosophers               |


Scenario Outline: Change a TODO's description that is associated with a project (Alternate Flow)
  Given the TODO "<todo_title>" is associated with the project "<project_title>"
  When the student updates the todo "<todo_title>" to have a new description "<new_description>"
  Then the todo "<todo_title>" should now have the description "<new_description>"
  And the student is notified that the update operation was successful

  Examples:
    | todo_title              | project_title       | new_description                                    |
    | Implement a linked list | Computer Science    | Super Advanced Data Structures and Algorithms      |
    | Summarize Hamlet        | English Literature  | Shakespearean drama and poetry                     |
    | Analyze time complexity | ECSE 202            | Analyze optimizations                              |
    | Think about stuff       | Philosophy 201      | Survey of Ancient thinkers                         |


Scenario Outline: Attempting to change the description of a non-existent TODO (Error Flow)
  Given no todo exists with the id "<id>"
  When the student updates the todo with id "<id>" to have a new description "<new_description>"
  Then the system should notify the student with the not found error message "<message>"

  Examples:
    | id  | new_description                      | message                               |
    | 99  | Trying to update invalid todo        | Invalid GUID for 99 entity todo       |
