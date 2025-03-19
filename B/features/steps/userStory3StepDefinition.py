from behave import given, when, then
import requests
from helperFunctions import get_todo_id_by_title

BASE_URL = "http://localhost:4567"

# Feature: Remove a TODO

# Normal Flow: Remove a TODO
@when('the student deletes the TODO with title "{todo_title}"')
def step_delete_todo_by_title(context, todo_title):
    todo_id = get_todo_id_by_title(todo_title)

    response = requests.delete(f"{BASE_URL}/todos/{todo_id}", headers={"Accept": "application/json"})
    context.response = response


@then('the TODO with the title "{todo_title}" should no longer exist')
def step_verify_todo_deleted(context, todo_title):
    todo_id = get_todo_id_by_title(todo_title)
    assert todo_id is None

@then("the student is notified that the removal operation was successful")
def step_verify_deletion_success(context):
    assert context.response.status_code == 200




# Error Flow: Remove a non-existent TODO
@when('the student deletes the TODO with id "{id}"')
def step_delete_todo_by_id(context, id):

    response = requests.delete(f"{BASE_URL}/todos/{id}", headers={"Accept": "application/json"})
    context.response = response




