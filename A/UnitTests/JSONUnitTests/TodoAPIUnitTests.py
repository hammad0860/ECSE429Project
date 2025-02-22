import unittest
import subprocess
import requests
import os
from deepdiff import DeepDiff

# Global Test Data Constants
BASE_URL = "http://localhost:4567"
TODOS_ENDPOINT = "/todos"
WORKING_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
APP_RUNNING = False
APP_PROCESS = None

# Expected JSON responses for GET requests
EXPECTED_TODOS_RESPONSE = {
    "todos": [
        {
            "id": "1",
            "title": "scan paperwork",
            "doneStatus": "false",
            "description": "",
            "categories": [{"id": "1"}],
            "tasksof": [{"id": "1"}]
        },
        {
            "id": "2",
            "title": "file paperwork",
            "doneStatus": "false",
            "description": "",
            "tasksof": [{"id": "1"}]
        }
    ]
}

# Expected response after the post operation
POST_EXPECTED_TODOS_RESPONSE = {
    "todos": [
        {
            "id": "1",
            "title": "scan paperwork",
            "doneStatus": "false",
            "description": "",
            "categories": [{"id": "1"}],
            "tasksof": [{"id": "1"}]
        },
        {
            "id": "2",
            "title": "file paperwork",
            "doneStatus": "false",
            "description": "",
            "tasksof": [{"id": "1"}]
        },
        {
            "id": "3",
            "title": "wash dishes",
            "doneStatus": "false",
            "description": ""
        }
    ]
}

# Expected response after the deletion operation
DELETE_EXPECTED_TODOS_RESPONSE = {
    "todos": [
        {
            "id": "1",
            "title": "scan paperwork",
            "doneStatus": "false",
            "description": "",
            "categories": [{"id": "1"}],
            "tasksof": [{"id": "1"}]
        }
    ]
}

# Payloads for POST/PUT operations
WASH_DISHES_PAYLOAD = {
    "title": "wash dishes",
    "doneStatus": False,
    "description": ""
}

WASH_DISHES_EXPECTED_RESPONSE = {
    "id": "3",
    "title": "wash dishes",
    "doneStatus": "false",
    "description": ""
}

UPDATE_SCAN_PAPERWORK_PAYLOAD = {
    "title": "scan paperwork",
    "doneStatus": True,
    "description": "all paperwork has been scanned"
}

UPDATED_SCAN_PAPERWORK_RESPONSE = {
    "id": "1",
    "title": "scan paperwork",
    "doneStatus": "true",
    "description": "all paperwork has been scanned",
    "categories": [{"id": "1"}],
    "tasksof": [{"id": "1"}]
}

# Expected JSON response after POST/PUT operations
UPDATED_TODOS_RESPONSE = {
    "todos": [
        {
            "id": "1",
            "title": "scan paperwork",
            "doneStatus": "true",
            "description": "all paperwork has been scanned",
            "categories": [{"id": "1"}],
            "tasksof": [{"id": "1"}]
        },
        {
            "id": "2",
            "title": "file paperwork",
            "doneStatus": "false",
            "description": "",
            "tasksof": [{"id": "1"}]
        }
    ]
}

# The below JSON is malformed since doneStatus is a string instead of a boolean
WASH_DISHES__MALFORMED_PAYLOAD = {
    "title": "wash dishes",
    "doneStatus": "false",
    "description": ""
}

class TodoApiUnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize testing data from constants
        cls.expectedTodosResponse = EXPECTED_TODOS_RESPONSE
        cls.washDishesPayload = WASH_DISHES_PAYLOAD
        cls.washDishesExpectedResponse = WASH_DISHES_EXPECTED_RESPONSE
        cls.updateScanPaperworkPayload = UPDATE_SCAN_PAPERWORK_PAYLOAD
        cls.updatedScanPaperworkResponse = UPDATED_SCAN_PAPERWORK_RESPONSE
        cls.updatedTodosResponse = UPDATED_TODOS_RESPONSE
        cls.postExpectedTodosResponse = POST_EXPECTED_TODOS_RESPONSE
        cls.deleteExpectedTodosResponse = DELETE_EXPECTED_TODOS_RESPONSE
        cls.malformedPayload = WASH_DISHES__MALFORMED_PAYLOAD

    def setUp(self):
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

    # Test: Get all TODOS
    def test_get_all_todos(self):
        response = requests.get(BASE_URL + TODOS_ENDPOINT, headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actualResponse = response.json()
        diff = DeepDiff(actualResponse, self.expectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})
        self.no_side_effects_for_non_modifying_requests(self)

    # Test: Get TODO by ID
    def test_get_todo_by_id(self):
        todo_id = 1
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actualResponse = response.json()
        diff = DeepDiff(actualResponse["todos"][0], self.expectedTodosResponse["todos"][0], ignore_order=True)
        self.assertEqual(diff, {})
        self.no_side_effects_for_non_modifying_requests(self)

    # Error Case Test: Get TODO by ID that does not exist
    def test_get_todo_by_non_existent_id(self):
        todo_id = 99
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 404)
        actualResponse = response.json()
        actual_error_message = actualResponse.get("errorMessages", [""])[0]
        expected_error_message = f"Could not find an instance with todos/{todo_id}"
        self.assertEqual(actual_error_message, expected_error_message)
        self.no_side_effects_for_non_modifying_requests(self)

    # Test: Get header for all TODOS
    def test_get_all_todos_header(self):
        response = requests.head(BASE_URL + TODOS_ENDPOINT, headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        self.no_side_effects_for_non_modifying_requests(self)

    # Test: Get header for TODO by ID
    def test_get_todo_by_id_header(self):
        todo_id = 1
        response = requests.head(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        self.no_side_effects_for_non_modifying_requests(self)

    # Error Case Test: Get header for TODO by non-existent ID
    def test_get_todo_by_non_existent_id_header(self):
        todo_id = 99
        response = requests.head(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 404)
        self.no_side_effects_for_non_modifying_requests(self)

    # Test: POST new TODO
    def test_post_new_todo(self):
        new_todo_id = 3
        response = requests.post(BASE_URL + TODOS_ENDPOINT, headers={"Accept": "application/json"}, json=self.washDishesPayload)
        self.assertEqual(response.status_code, 201)
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}/{new_todo_id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actualResponse = response.json()
        diff = DeepDiff(actualResponse["todos"][0], self.washDishesExpectedResponse, ignore_order=True)
        self.assertEqual(diff, {})
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/json"})
        diff = DeepDiff(response.json(), self.postExpectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

    # Test: POST update TODO by ID
    def test_post_update_todo_by_id(self):
        todo_id = 1
        response = requests.post(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/json"}, json=self.updateScanPaperworkPayload)
        self.assertEqual(response.status_code, 200)
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actualResponse = response.json()
        diff = DeepDiff(actualResponse["todos"][0], self.updatedScanPaperworkResponse, ignore_order=True)
        self.assertEqual(diff, {})
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/json"})
        diff = DeepDiff(response.json(), self.updatedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

    # Test: POST update TODO by non existent ID
    def test_post_update_todo_by_nonexistent_id(self):
        todo_id = 99
        response = requests.post(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/json"}, json=self.updateScanPaperworkPayload)
        self.assertEqual(response.status_code, 404)
        actualResponse = response.json()
        expectedError = {"errorMessages": [f'No such todo entity instance with GUID or ID {todo_id} found']}
        self.assertEqual(actualResponse, expectedError)
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/json"})
        diff = DeepDiff(response.json(), self.expectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

    # Test: POST update TODO by malformed JSON
    def test_post_update_todo_by_malformed_json(self):
        todo_id = 1
        response = requests.post(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/json"}, json=self.malformedPayload)
        self.assertEqual(response.status_code, 400)
        actualResponse = response.json()
        expectedError = {"errorMessages": [f'Failed Validation: doneStatus should be BOOLEAN']}
        self.assertEqual(actualResponse, expectedError)
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/json"})
        diff = DeepDiff(response.json(), self.expectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

    # Test: PUT update TODO by ID
    def test_put_update_todo_by_id(self):
        todo_id = 1
        response = requests.put(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/json"}, json=self.updateScanPaperworkPayload)
        self.assertEqual(response.status_code, 200)
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actualResponse = response.json()
        diff = DeepDiff(actualResponse["todos"][0], self.updatedScanPaperworkResponse, ignore_order=True)
        self.assertEqual(diff, {})
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/json"})
        diff = DeepDiff(response.json(), self.updatedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

    # Error Case Test: PUT update TODO by non existent ID
    def test_put_update_todo_by_nonexistent_id(self):
        todo_id = 99
        response = requests.put(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/json"}, json=self.updateScanPaperworkPayload)
        self.assertEqual(response.status_code, 404)
        actualResponse = response.json()
        expectedError = {"errorMessages": [f'Invalid GUID for {todo_id} entity todo']}
        self.assertEqual(actualResponse, expectedError)
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/json"})
        diff = DeepDiff(response.json(), self.expectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

    # Error Case Test: PUT update TODO by malformed JSON
    def test_put_update_todo_by_malformed_json(self):
        todo_id = 1
        response = requests.put(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/json"}, json=self.malformedPayload)
        self.assertEqual(response.status_code, 400)
        actualResponse = response.json()
        expectedError = {"errorMessages": [f'Failed Validation: doneStatus should be BOOLEAN']}
        self.assertEqual(actualResponse, expectedError)
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/json"})
        diff = DeepDiff(response.json(), self.expectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

    # Test: DELETE TODO by ID
    def test_delete_todo_by_id(self):
        todo_id = 2
        response = requests.delete(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 404)
        expectedError = {"errorMessages": [f"Could not find an instance with todos/{todo_id}"]}
        actualResponse = response.json()
        self.assertEqual(actualResponse, expectedError)
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/json"})
        diff = DeepDiff(response.json(), self.deleteExpectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

    # Error Case Test: DELETE TODO by non existent ID
    def test_delete_todo_by_nonexistent_id(self):
        todo_id = 99
        response = requests.delete(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 404)
        expectedError = {"errorMessages": [f"Could not find any instances with todos/{todo_id}"]}
        actualResponse = response.json()
        self.assertEqual(actualResponse, expectedError)
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/json"})
        diff = DeepDiff(response.json(), self.expectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

    @staticmethod
    def server_running():
        try:
            response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}", timeout=3)
        except requests.exceptions.RequestException:
            return False
        return True

    @staticmethod
    def wait_for_server():
        while True:
            response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}", timeout=3)
            if response.status_code == 200:
                return

    # Assert that there are no unexpected side effects for non-modifying requests
    @staticmethod
    def no_side_effects_for_non_modifying_requests(self):
        response = requests.get(BASE_URL + TODOS_ENDPOINT, headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actualResponse = response.json()
        diff = DeepDiff(actualResponse, self.expectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

if __name__ == '__main__':
    unittest.main()
