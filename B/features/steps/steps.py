from behave import given, when, then
import requests
from distutils.util import strtobool
from helperFunctions import get_todo_id_by_title, get_project_id_by_title


BASE_URL = "http://localhost:4567"



# Checks if GET /todos returns 200, meaning server is up.
# Used for all of the features
@given("the server is running")
def step_server_running(context):
    response = requests.get(f"{BASE_URL}/todos")
    assert response.status_code == 200

# Used for the features 1, 2, 3, 4
@given("the following TODOs exist")
def step_todos_exist(context):
    for row in context.table:
        todo_data = {
            "title": row["todo_title"],
            "doneStatus": bool(strtobool(row["doneStatus"])),  
            "description": row["description"]
        }
        response = requests.post(
            f"{BASE_URL}/todos",
            json=todo_data,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 201


# Used for the features 1, 2, 3, 4
@given("the following projects exist")
def step_projects_exist(context):

    for row in context.table:
        project_data = {
            "title": row["project_title"],
            "completed": bool(strtobool(row["completed"])),
            "description": row["description"],
            "active": bool(strtobool(row["active"])),
        }
        response = requests.post(
            f"{BASE_URL}/projects",
            json=project_data,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        assert response.status_code == 201


# Used for the features 1, 2, 3, 4
@given('the TODO "{todo_title}" is associated with the project "{project_title}"')
def step_associate_todo_with_project(context, project_title, todo_title):

    todo_id = get_todo_id_by_title(todo_title)
    project_id = get_project_id_by_title(project_title)

    relationship_data = {"id": project_id}

    response = requests.post(
        f"{BASE_URL}/todos/{todo_id}/tasksof",
        json=relationship_data,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )

    assert response.status_code == 201


# Used for the features 1, 2, 3, 4
@given('no TODO exists with the id "{id}"')
def step_non_existent_task(context, id):

    response = requests.get(f"{BASE_URL}/todos/{id}")
    assert response.status_code == 404


# Used for the features 1, 2
@then("the student is notified that the update operation was successful")
def step_verify_project_update_success_notification(context):

    assert context.response.status_code == 200

# Used for the features 1, 2, 3, 4
@then('the system should notify the student with the not found error message "{message}"')
def step_verify_error_message(context, message):
 
    assert context.response.status_code  == 404 
    error_data = context.response.json()

    error_message = error_data.get("errorMessages")[0]
    
    
    assert message == error_message




    
