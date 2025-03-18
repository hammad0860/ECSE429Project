Feature: Creating a New TODO
  As a student, I want to create a new TODO, so that I can add new tasks to my list.

Background:
  Given the server is running
    And the following TODOS exist:
        | todo_title               | doneStatus | description                     |
        | Implement a linked list  | false      | data structure assignment       |
        | Analyze time complexity  | false      | O(n) vs O(log n) analysis       |
        | Summarize Hamlet         | false      | Focus on Act 3                  |
        | Think about stuff        | false      | dont think too much             |


Scenario Outline: Create a New TODO with a title and description (Normal Flow)
  When the student creates a new TODO with todo_title "<todo_title>" and description "<description>"
  Then a new TODO with todo_title "<todo_title>" should exist with doneStatus "false" and description "<description>"
  And the student is notified that the creation operation was successful

  Examples:
    | todo_title               | description                     |
    | Implement a linked list  | data structure assignment       |
    | Analyze time complexity  | O(n) vs O(log n) analysis       |
    | Summarize Hamlet         | Focus on Act 3                  |
    | Think about stuff        | dont think too much             |


Scenario Outline: Create a New TODO with only a title (Alternate Flow)
  When the student creates a new TODO with todo_title "<todo_title>" and no description
  Then a new TODO with todo_title "<todo_title>" should exist with doneStatus "false" and an empty description
  And the student is notified that the creation operation was successful

  Examples:
    | todo_title               |
    | Implement a linked list  |
    | Analyze time complexity  |
    | Summarize Hamlet         |
    | Think about stuff        |


Scenario Outline: Attempt to create a new TODO with an invalid doneStatus value (Error Flow)
  Given the server is running
  When the student creates a new TODO with todo_title "<todo_title>", description "<description>" and doneStatus "<doneStatus>"
  Then the system should notify the student with the error message "<error_message>"

  Examples:
    | todo_title              | description          | doneStatus | error_message                                             |
    | Implement a linked list | Some description     | invalid    | Failed Validation: doneStatus should be BOOLEAN           |

