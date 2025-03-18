from behave import given, when, then
import requests
from helperFunctions import get_todo_id_by_title

BASE_URL = "http://localhost:4567"



# Feature: Update a TODO's description

# Normal Flow: Update a TODO's description
@when('the student updates the todo "{todo_title}" to have a new description "{new_description}"')
def step_update_project_description_by_title(context, todo_title, new_description):

    todo_id = get_todo_id_by_title(todo_title)

    update_data = {
        "title": todo_title,
        "description": new_description
    }

    response = requests.put(
        f"{BASE_URL}/todos/{todo_id}",
        json=update_data,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    context.response = response

    assert response.status_code == 200 


@then('the todo "{todo_title}" should now have the description "{new_description}"')
def step_verify_todo_description(context, todo_title, new_description):

    todo_id = get_todo_id_by_title(todo_title)

    response = requests.get(
        f"{BASE_URL}/todos/{todo_id}",
        headers={"Accept": "application/json"}
    )
    assert response.status_code == 200

    todo_data = response.json().get("todos", [])

    updated_desc = todo_data[0].get("description", "")
    assert updated_desc == new_description





# Error Flow: Update a non-existent TODO's description

@when('the student updates the todo with id "{id}" to have a new description "{new_description}"')
def step_update_non_existent_todo(context, id, new_description):
    update_data = {"description": new_description}
    response = requests.put(
        f"{BASE_URL}/todos/{id}",
        json=update_data,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    context.response = response









