from behave import given, when, then
import requests
import os
from distutils.util import strtobool
from helperFunctions import get_todo_id_by_title


BASE_URL = "http://localhost:4567"

# Feature: Mark a TODO as done

# Normal Flow: Mark a standalone TODO as done
@when('the student updates the doneStatus status of the TODO with title "{todo_title}" to "{doneStatus}"')
def step_update_todo_status(context, todo_title, doneStatus):
    todo_id = get_todo_id_by_title(todo_title)

    update_data = {
        "title": f"{todo_title}",
        "doneStatus": bool(strtobool(doneStatus))
        
    }


    response = requests.get(f"{BASE_URL}/todos/{todo_id}", headers={"Accept": "application/json"})

    response = requests.put(
        f"{BASE_URL}/todos/{todo_id}",
        json=update_data,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )

    assert response.status_code == 200
    context.response = response


@then('the TODO with the title "{todo_title}" should now have a doneStatus status of "{doneStatus}"')
def step_verify_todo_status(context, todo_title, doneStatus):

    todo_id = get_todo_id_by_title(todo_title)

    response = requests.get(f"{BASE_URL}/todos/{todo_id}", headers={"Accept": "application/json"})

    todo_obj = response.json()
    expected_bool =doneStatus.lower()

    assert todo_obj["todos"][0]["doneStatus"] == expected_bool
    



    


# Alternate Flow: Mark a project-associated TODO as done 
@when('the student updates the doneStatus status of the associated TODO with title "{todo_title}" to "{doneStatus}"')
def step_update_todo_associated_with_project(context, todo_title, doneStatus):

    todo_id = get_todo_id_by_title(todo_title)

    bool_value =  bool(strtobool(doneStatus))

    update_data = {"doneStatus": bool_value,
                   "title": todo_title
    }

    response = requests.put(
        f"{BASE_URL}/todos/{todo_id}",
        json=update_data,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )

    assert response.status_code == 200
    context.response = response


@then('the associated TODO with the title "{todo_title}" should now have a doneStatus status of "{doneStatus}"')
def step_verify_associated_todo_status(context, todo_title, doneStatus):

    todo_id = get_todo_id_by_title(todo_title)

    response = requests.get(f"{BASE_URL}/todos/{todo_id}", headers={"Accept": "application/json"})

    todo_obj = response.json()
    expected_bool = doneStatus.lower() 

    assert todo_obj["todos"][0]["doneStatus"] == expected_bool


# Error Flow: Attempt to mark a non-existent TODO as done
@when('the student updates the doneStatus status of the TODO with id "{id}" to "{doneStatus}"')
def step_update_nonexistent_task(context, id, doneStatus):
    bool_value = bool(strtobool(doneStatus))
    update_data = {"doneStatus": bool_value}

    response = requests.put(
        f"{BASE_URL}/todos/{id}",
        json=update_data,
        headers={"Content-Type": "application/json"}
    )
    assert(response.status_code == 404)
    context.response = response

