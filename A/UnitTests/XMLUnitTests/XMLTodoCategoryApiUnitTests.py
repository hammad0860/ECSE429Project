import json
import unittest
import subprocess
import requests
import os
from deepdiff import DeepDiff
import xml.etree.ElementTree as ET
from xmljson import parker

# Global Test Data Constants
BASE_URL = "http://localhost:4567"
TODOS_ENDPOINT = "/todos"
WORKING_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
APP_RUNNING = False
APP_PROCESS = None

# Expected responses (using JSON-like dictionaries)
EXPECTED_JSON_ALL_IDS = {
    "todo": [
        {
            "id": 1,
            "title": "scan paperwork",
            "doneStatus": False,
            "description": None,
            "categories": {
                "id": 1,
                "title": "Office",
                "description": None
            },
            "tasksof": {"id": "1"}
        },
        {
            "id": 2,
            "title": "file paperwork",
            "doneStatus": False,
            "description": None,
            "tasksof": {"id": 1}
        }
    ]
}

HOME_CATEGORY = {
    "id": 2,
    "title": "Home",
    "description": None
}

UPDATED_ALL_IDS_JSON = {
    "todo": [
        {
            "id": 1,
            "title": "scan paperwork",
            "doneStatus": False,
            "description": None,
            "tasksof": {"id": 1}
        },
        {
            "id": 2,
            "title": "file paperwork",
            "doneStatus": False,
            "description": None,
            "tasksof": {"id": 1}
        }
    ]
}

POST_UPDATED_JSON_ALL_IDS = {
    "todo": [
        {
            "id": 1,
            "title": "scan paperwork",
            "doneStatus": False,
            "description": None,
            "categories": {"id": 1},
            "tasksof": {"id": "1"}
        },
        {
            "id": 2,
            "title": "file paperwork",
            "doneStatus": False,
            "description": None,
            "categories": {"id": 2},
            "tasksof": {"id": 1}
        }
    ]
}

class TodoApiUnitTests(unittest.TestCase):

    def setUp(self):
        global EXPECTED_JSON_ALL_IDS, HOME_CATEGORY, UPDATED_ALL_IDS_JSON, POST_UPDATED_JSON_ALL_IDS
        self.expected_json_all_ids = EXPECTED_JSON_ALL_IDS
        self.home_category = HOME_CATEGORY
        self.updated_all_ids_json = UPDATED_ALL_IDS_JSON
        self.post_updated_json_all_ids = POST_UPDATED_JSON_ALL_IDS

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

    # Tests getting cateogries for a specific TODO
    def test_get_todo_categories(self):
        todo_id = 1
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 200)
        
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        # Ensure the response is as expected
        diff = DeepDiff(actualResponse["category"], self.expected_json_all_ids["todo"][0]["categories"], ignore_order=True)
        self.assertEqual(diff, {})

        # Ensures there are no side effects after the request
        self.no_side_effects_for_non_modifying_requests(self)
    
    # Tests getting categories for a specific TODO with a nonexistent ID
    # Note: This test is implemented with the expected output and fails due to a bug
    def test_get_todo_categories_non_existent_id_bug(self):
        todo_id = 99
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/xml"})
        # Expected 404 but returns 200
        self.assertEqual(response.status_code, 404)
        self.no_side_effects_for_non_modifying_requests(self)

    # Note: This test is designed to pass for the bug and verifies the actual behaviour
    def test_get_todo_categories_non_existent_id_sucess(self):
        todo_id = 99
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/xml"})    
        # Expected 404 but returns 200
        self.assertEqual(response.status_code, 200)
        self.no_side_effects_for_non_modifying_requests(self)

    # Tests getting head of cateogries for a specific TODO and cateogry
    def test_head_todo_categories(self):
        todo_id = 1
        response = requests.head(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 200)
        self.no_side_effects_for_non_modifying_requests(self)

    # Tests head of cateogries for a specific TODO with a nonexistent ID
    # Note: This test is implemented with the expected output and fails due to a bug
    def test_head_todo_categories_non_existent_id_bug(self):
        todo_id = 99
        response = requests.head(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/xml"})
        # Expected 404 but returns 200
        self.assertEqual(response.status_code, 404)
        self.no_side_effects_for_non_modifying_requests(self)

    # Tests head of cateogries for a specific TODO with a nonexistent ID
    # Note: This test is designed to pass and verifies the actual (buggy) behvaiour
    def test_head_todo_categories_non_existent_id_sucess(self):
        todo_id = 99
        response = requests.head(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/xml"})
        # Expected 404 but returns 200
        self.assertEqual(response.status_code, 200)
        self.no_side_effects_for_non_modifying_requests(self)

    # Tests posting a new todo cateogry relationship isntance for a specific TODO with an ID
    # Note: This test is implemented with the expected output and fails due to a bug
    def test_post_todo_categories_bug(self):
        todo_id = 2

        xml_payload = """<category>
                        <description>None</description>
                        <id>2</id>
                        <title>Home</title>
                        </category>"""
        
        response = requests.post(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}/categories", 
                                 headers={"Accept": "application/xml", "Content-Type": "application/xml"}, data=xml_payload)

        self.assertEqual(response.status_code, 201)

        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 200)
        
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        
        # Ensure that the post request actually makes the specified changes
        diff = DeepDiff(actualResponse["category"][0], self.home_category, ignore_order=True)
        self.assertEqual(diff, {})

        # Ensures there are no side effects after the request
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        diff = DeepDiff(actual_json, self.post_updated_json_all_ids, ignore_order=True)
        self.assertEqual(diff, {})
       
    # Tests posting a new todo cateogry relationship isntance for a specific TODO with an ID
    # Note: This test is designed to pass and verifies the actual (buggy) behvaiour
    def test_post_todo_categories_success(self):
        todo_id = 2

        xml_payload = """<category>
                        <description>None</description>
                        <id>2</id>
                        <title>Home</title>
                        </category>"""
        
        response = requests.post(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}/categories", 
                                 headers={"Accept": "application/xml", "Content-Type": "application/xml"}, data=xml_payload)

        self.assertEqual(response.status_code, 404)
        self.no_side_effects_for_non_modifying_requests(self)

    # Test: DELETE a todo's category by id
    def test_delete_todo_categories(self):
        todo_id = 1
        response = requests.delete(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories/{todo_id}", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 200)
        
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 200)

        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        
        # Ensures there are no side effects after the request
        diff = DeepDiff(actualResponse, self.updated_all_ids_json, ignore_order=True)
        self.assertEqual(diff, {})

    # Error Case Test: DELETE a todo's category by id
    def test_delete_todo_categories_non__existent_id(self):
        todo_id = 99
        response = requests.delete(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories/{todo_id}", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 404)
        self.no_side_effects_for_non_modifying_requests(self)
        
    # Error Case Test: DELETE a specific todo's category by id two times
    def test_delete_todo_categories_double(self):
        todo_id = 1
        response = requests.delete(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories/{todo_id}", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 200)
        response = requests.delete(f"{BASE_URL}{TODOS_ENDPOINT}/{todo_id}/categories/{todo_id}", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 404)

    # Assert that there are no unexpected side effects for non-modifying requests
    @staticmethod
    def no_side_effects_for_non_modifying_requests(self):
        # Verifies that first todo has the expected categories
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}/1/categories", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 200)
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        # Ensure the response is as expected
        diff = DeepDiff(actualResponse["category"], self.expected_json_all_ids["todo"][0]["categories"], ignore_order=True)
        self.assertEqual(diff, {})

        # Verifies that second todo has the expected categories  
        response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}/2/categories", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 200)
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        # Ensure the response is as expected
        self.assertEqual(actualResponse, None)
    
    @staticmethod
    def wait_for_server():
        while True:
            response = requests.get(f"{BASE_URL}{TODOS_ENDPOINT}", timeout=3)
            if response.status_code == 200:
                return

if __name__ == '__main__':
    unittest.main()





