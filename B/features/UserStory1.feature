Feature: Marking finished TODOs
  As a student, I want to mark TODOs as done once I'm done with them, so I can track my progress more efficiently.

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

Scenario Outline: Mark a TODO as done (Normal Flow)
  When the student updates the doneStatus status of the TODO with title "<todo_title>" to "<doneStatus>"
  Then the TODO with the title "<todo_title>" should now have a doneStatus status of "<doneStatus>"
  And the student is notified that the update operation was successful

  Examples:
    | todo_title               | doneStatus | 
    | Implement a linked list  | true       | 
    | Analyze time complexity  | true       | 
    | Summarize Hamlet         | true       |
    | Think about stuff        | true       |

Scenario Outline: Mark a project-associated TODO as done (Alternate Flow)
  Given the TODO "<todo_title>" is associated with the project "<project_title>"
  When the student updates the doneStatus status of the associated TODO with title "<todo_title>" to "<doneStatus>"
  Then the associated TODO with the title "<todo_title>" should now have a doneStatus status of "<doneStatus>"
  And the student is notified that the update operation was successful

  Examples:
    | todo_title               |project_title     | doneStatus | 
    | Implement a linked list  |Computer Science  | true       | 
    | Analyze time complexity  |ECSE 202          | true       | 
    | Summarize Hamlet         |English Literature| true       |
    | Think about stuff        |Philosophy 201    | true       |

Scenario Outline: Attempting to mark a non-existent TODO as done (Error Flow)
  Given no TODO exists with the id "<id>"
  When the student updates the doneStatus status of the TODO with id "<id>" to "<doneStatus>"
  Then the system should notify the student with the not found error message "<message>"

  Examples:
    | id  | doneStatus | message                                               |
    | 99  | true       | Invalid GUID for 99 entity todo                       |

