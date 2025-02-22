import unittest
import subprocess
import requests
import os
from deepdiff import DeepDiff

# Global Test Data Constants

BASE_URL = "http://localhost:4567"
TODOS_ENDPOINT = "/todos"
WORKING_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
APP_RUNNING = False
APP_PROCESS = None

EXPECTED_JSON_ALL_IDS = {
    "todos": [
        {
            "id": "1",
            "title": "scan paperwork",
            "doneStatus": "false",
            "description": "",
            "categories": [{
                "id": "1",
                "title": "Office",
                "description": ""
            }],
            "tasksof": [{
                "id": "1",
                "title": "Office Work",
                "completed": "false",
                "active": "false",
                "description": "",
                "tasks": [
                    {
                        "id": "1"
                    },
                    {
                        "id": "2"
                    }
                ]
            }]
        },
        {
            "id": "2",
            "title": "file paperwork",
            "doneStatus": "false",
            "description": "",
            "tasksof": [{
                "id": "1",
                "title": "Office Work",
                "completed": "false",
                "active": "false",
                "description": "",
                "tasks": [
                    {
                        "id": "1"
                    },
                    {
                        "id": "2"
                    }
                ]
            }]
        }
    ]
}

GET_TODO_PROJECTS_RESPONSE = {
    "projects": [
        {
            "id": "1",
            "title": "Office Work",
            "completed": "false",
            "active": "false",
            "description": "",
            "tasks": [
                {
                    "id": "1"
                },
                {
                    "id": "2"
                }
            ]
        },
        {
            "id": "1",
            "title": "Office Work",
            "completed": "false",
            "active": "false",
            "description": "",
            "tasks": [
                {
                    "id": "1"
                },
                {
                    "id": "2"
                }
            ]
        }
    ]
}

class TodoApiUnitTests(unittest.TestCase):

    def setUp(self):
        global EXPECTED_JSON_ALL_IDS, GET_TODO_PROJECTS_RESPONSE

        self.expected_json_all_ids = EXPECTED_JSON_ALL_IDS
        self.get_todo_projects_response = GET_TODO_PROJECTS_RESPONSE

        global APP_RUNNING, APP_PROCESS
        if not APP_RUNNING:
            try:
                APP_PROCESS = subprocess.Popen(
                    ["java", "-jar", os.path.join(WORKING_DIRECTORY, "runTodoManagerRestAPI-1.5.5.jar")],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    cwd=WORKING_DIRECTORY,
                    shell=True
                )
                self.wait_for_server()    
                APP_RUNNING = True
            except Exception as e:
                APP_RUNNING = False
        
        if not APP_RUNNING:
            raise RuntimeError("The application could not be started and the unit tests have been terminated.")

    # Gets all projects for a todo
    def test_get_todo_projects(self):
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}/tasksof", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        diff = DeepDiff(actual_json, self.get_todo_projects_response, ignore_order=True)
        self.assertEqual(diff, {})

        # Ensures there are no side effects after the request
        self.no_side_effects_for_non_modifying_requests(self)

    def tearDown(self):
        global APP_RUNNING, APP_PROCESS
        try:
            requests.get(f"{BASE_URL}/shutdown")
        except Exception:
            pass

        APP_PROCESS.terminate()  
        APP_PROCESS.wait()
        APP_PROCESS = None
        APP_RUNNING = False

    # Assert that there are no unexpected side effects for non-modifying requests
    @staticmethod
    def no_side_effects_for_non_modifying_requests(self):
        # Verifies that first todo has the expected tasksof
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}/1/tasksof", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        diff = DeepDiff(actual_json["projects"], self.expected_json_all_ids["todos"][0]["tasksof"], ignore_order=True)
        self.assertEqual(diff, {})

        # Verifies that second todo has the expected tasksof  
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}/2/tasksof", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        diff = DeepDiff(actual_json["projects"], self.expected_json_all_ids["todos"][1]["tasksof"], ignore_order=True)
        self.assertEqual(diff, {})

    @staticmethod
    def wait_for_server():
        while True:
            response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}", timeout=3)
            if response.status_code == 200:
                return

if __name__ == '__main__':
    unittest.main()
