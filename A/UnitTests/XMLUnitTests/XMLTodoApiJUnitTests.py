import json
import unittest
import subprocess
import requests
import os
from deepdiff import DeepDiff
from xmljson import badgerfish as bf
import xml.etree.ElementTree as ET
from xmljson import parker



# Global Test Data Constants
BASE_URL = "http://localhost:4567"
TODOS_ENDPOINT = "/todos"
WORKING_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
APP_RUNNING = False
APP_PROCESS = None

# Expected JSON responses for GET requests
EXPECTED_TODOS_RESPONSE = {
    "todo": [
        {
            "id": 1,
            "title": "scan paperwork",
            "doneStatus": False,
            "description": None,
            "categories": {"id": 1},
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

# Expected response after the post operation
POST_EXPECTED_TODOS_RESPONSE = {
    "todo": [
        {
            "id": 1,
            "title": "scan paperwork",
            "doneStatus": False,
            "description": None,
            "categories": {"id": 1},
            "tasksof": {"id": 1}
        },
        {
            "id": 2,
            "title": "file paperwork",
            "doneStatus": False,
            "description": None,
            "tasksof": {"id": 1}
        },
        {
            "id": 3,
            "title": "wash dishes",
            "doneStatus": False,
            "description": None
        }
    ]
}

# Expected response after the deletion operation
DELETE_EXPECTED_TODOS_RESPONSE = {
    "todo": {
        "id": 1,
        "title": "scan paperwork",
        "doneStatus": False,
        "description": None,
        "categories": {"id": 1},
        "tasksof": {"id": 1}
    }
}

# Payloads for POST/PUT operations
WASH_DISHES_PAYLOAD = {
    "title": "wash dishes",
    "doneStatus": False,
    "description": ""
}

WASH_DISHES_EXPECTED_RESPONSE = {
    "id": 3,
    "title": "wash dishes",
    "doneStatus": False,
    "description": None
}

UPDATE_SCAN_PAPERWORK_PAYLOAD = {
    "title": "scan paperwork",
    "doneStatus": True,
    "description": "all paperwork has been scanned"
}

UPDATED_SCAN_PAPERWORK_RESPONSE = {
    "id": 1,
    "title": "scan paperwork",
    "doneStatus": True,
    "description": "all paperwork has been scanned",
    "categories": {"id": 1},
    "tasksof": {"id": 1}
}

# The below JSON is malformed since doneStatus is a string instead of a boolean
WASH_DISHES__MALFORMED_PAYLOAD = {
    "title": "wash dishes",
    "doneStatus": "false",
    "description": ""
}

# Expected JSON response after POST/PUT operations
UPDATED_TODOS_RESPONSE = {
    "todo": [
        {
            "id": 1,
            "title": "scan paperwork",
            "doneStatus": True,
            "description": "all paperwork has been scanned",
            "categories": {"id": 1},
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

UPDATED_TODO_PUT_RESPONSE = {
    'todo': {
        'doneStatus': True,
        'description': 'all paperwork has been scanned', 
        'id': 1, 
        'title': 'scan paperwork'
    }
}

UPDATED_TODO_PUT_ENVIRONMENT = {
    'todo': [
        {
            'doneStatus': False, 
            'description': None, 
            'tasksof': {'id': 1}, 
            'id': 2, 
            'title': 'file paperwork'
        },
        {
            'doneStatus': True, 
            'description': 'all paperwork has been scanned',
            'id': 1, 
            'title': 'scan paperwork'
        }
    ]
}


# Unit Test Class
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
        cls.updated_todo_put_response = UPDATED_TODO_PUT_RESPONSE
        cls.updated_todo_put_environment = UPDATED_TODO_PUT_ENVIRONMENT

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
        response = requests.get(BASE_URL + TODOS_ENDPOINT, headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 200)
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        # Ensure the response is as expected
        diff = DeepDiff(actualResponse, self.expectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})
        
        self.no_side_effects_for_non_modifying_requests(self)

    # Test: Get TODO by ID
    def test_get_todo_by_id(self):
        todo_id = 1
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 200)
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        # Ensure the response is as expected
        diff = DeepDiff(actualResponse["todo"], self.expectedTodosResponse["todo"][0], ignore_order=True)
        self.assertEqual(diff, {})
        self.no_side_effects_for_non_modifying_requests(self)

    # Error Case Test: Get TODO by ID that does not exist
    def test_get_todo_by_non_existent_id(self):
        todo_id = 99
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 404)
        self.no_side_effects_for_non_modifying_requests(self)

    # Test: Get header for all TODOS
    def test_get_all_todos_header(self):
        response = requests.head(BASE_URL + TODOS_ENDPOINT, headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 200)
        self.no_side_effects_for_non_modifying_requests(self)

    # Test: Get header for TODO by ID
    def test_get_todo_by_id_header(self):
        todo_id = 1
        response = requests.head(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 200)
        self.no_side_effects_for_non_modifying_requests(self)
    
    # Error Case Test: Get header for TODO by non-existent ID
    def test_get_todo_by_non_existent_id_header(self):
        todo_id = 99
        response = requests.head(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 404)
        self.no_side_effects_for_non_modifying_requests(self)

    # Test: POST new TODO
    def test_post_new_todo(self):
        new_todo_id = 3
        response = requests.post(BASE_URL + TODOS_ENDPOINT, headers={"Accept": "application/xml"}, json=self.washDishesPayload)
        self.assertEqual(response.status_code, 201)
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}/{new_todo_id}", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 200)
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        # Ensure the modification is as expected
        diff = DeepDiff(actualResponse["todo"], self.washDishesExpectedResponse, ignore_order=True)
        self.assertEqual(diff, {})

        # Now check to ensure there are no unexpected side effects for the post request
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/xml"})
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        diff = DeepDiff(actualResponse, self.postExpectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

    # Test: POST update TODO by ID
    def test_post_update_todo_by_id(self):
        todo_id = 1
        xml_payload = """<todo>
        <title>scan paperwork</title>
        <doneStatus>true</doneStatus>
        <description>all paperwork has been scanned</description>
        </todo>"""

        response = requests.post(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", 
        headers={"Accept": "application/xml","Content-Type": "application/xml"}, data=xml_payload)
        self.assertEqual(response.status_code, 200)
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 200)
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        # Ensure the modification is as expected       
        diff = DeepDiff(actualResponse["todo"], self.updatedScanPaperworkResponse, ignore_order=True)
        self.assertEqual(diff, {})
    
        # Now check to ensure there are no unexpected side effects for the post request
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/xml"})
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        diff = DeepDiff(actualResponse, self.updatedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

    # Test: POST update TODO by non existtent ID
    def test_post_update_todo_by_nonexistent_id(self):
        todo_id = 99
        xml_payload = """<todo>
        <title>scan paperwork</title>
        <doneStatus>true</doneStatus>
        <description>all paperwork has been scanned</description>
        </todo>"""

        response = requests.post(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", 
        headers={"Accept": "application/xml","Content-Type": "application/xml"}, data=xml_payload)
        self.assertEqual(response.status_code, 404)

        # Now check to sensure there are no unexpected side effects for the post request
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/xml"})
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        diff = DeepDiff(actualResponse, self.expectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

    # Test: POST update TODO by malformed JSON
    def test_post_update_todo_by_malformed_json(self):
        todo_id = 1
        xml_payload = """<todo>
        <title>scan paperwork</title>
        <doneStatus>true</doneStatus>
        <invalidField>invalid</invalidField>
        <description>all paperwork has been scanned</description>
        </todo>"""

        response = requests.post(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", 
        headers={"Accept": "application/xml","Content-Type": "application/xml"}, data=xml_payload)
        self.assertEqual(response.status_code, 400)
    
        # Now check to sensure there are no unexpected side effects for the post request
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/xml"})
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        diff = DeepDiff(actualResponse, self.expectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

    # Test: PUT update TODO by ID
    def test_put_update_todo_by_id(self):
        todo_id = 1
        xml_payload = """<todo>
        <title>scan paperwork</title>
        <doneStatus>true</doneStatus>
        <description>all paperwork has been scanned</description>
        </todo>"""

        response = requests.put(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", 
        headers={"Accept": "application/xml","Content-Type": "application/xml"}, data=xml_payload)
        self.assertEqual(response.status_code, 200)
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 200)
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        # Ensure the modification is as expected       
        diff = DeepDiff(actualResponse, self.updated_todo_put_response, ignore_order=True)
        self.assertEqual(diff, {})

        # Now check to sensure there are no unexpected side effects for the put request
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/xml"})
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        diff = DeepDiff(actualResponse, self.updated_todo_put_environment, ignore_order=True)
        self.assertEqual(diff, {})

    # Error Case Test: PUT update TODO by non existtent ID
    def test_put_update_todo_by_nonexistent_id(self):
        todo_id = 99
        xml_payload = """<todo>
        <title>scan paperwork</title>
        <doneStatus>true</doneStatus>
        <description>all paperwork has been scanned</description>
        </todo>"""

        response = requests.put(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", 
        headers={"Accept": "application/xml","Content-Type": "application/xml"}, data=xml_payload)
        self.assertEqual(response.status_code, 404)

        # Now check to sensure there are no unexpected side effects for the put request
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/xml"})
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        diff = DeepDiff(actualResponse, self.expectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

    # Test: PUT update TODO by malformed xml
    def test_put_update_todo_by_malformed_xml(self):
        todo_id = 1
        xml_payload = """<todo>
        <title>scan paperwork</title>
        <doneStatus>true</doneStatus>
        <invalidField>invalid</invalidField>
        <description>all paperwork has been scanned</description>
        </todo>"""

        response = requests.put(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", 
        headers={"Accept": "application/xml","Content-Type": "application/xml"}, data=xml_payload)
        self.assertEqual(response.status_code, 400)
    
        # Now check to sensure there are no unexpected side effects for the put request
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/xml"})
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        diff = DeepDiff(actualResponse, self.expectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

    # Test: DELETE TODO by ID
    def test_delete_todo_by_id(self):
        todo_id = 2
        response = requests.delete(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/xml"})
        self.assertEqual(response.status_code, 200)
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/xml"})
        # Ensure the deletion is as expected
        self.assertEqual(response.status_code, 404)

        # Now check to sensure there are no unexpected side effects for the delete request
        response = requests.get(BASE_URL + f"{TODOS_ENDPOINT}", headers={"Accept": "application/xml"})
        # Convert xml response into json format
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        diff = DeepDiff(actualResponse, self.deleteExpectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

    # Error Case Test: DELETE TODO by non existent ID
    def test_delete_todo_by_nonexistent_id(self):
        todo_id = 99
        response = requests.delete(BASE_URL + f"{TODOS_ENDPOINT}/{todo_id}", headers={"Accept": "application/XML"})
        self.assertEqual(response.status_code, 404)
        self.no_side_effects_for_non_modifying_requests(self)
    
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
        response = requests.get(BASE_URL + TODOS_ENDPOINT, headers={"Accept": "application/xml"})
        actualResponse = ET.fromstring(response.content)
        actualResponse = parker.data(actualResponse)
        actualResponse = json.loads(json.dumps(actualResponse))
        # Ensure the response is as expected
        diff = DeepDiff(actualResponse, self.expectedTodosResponse, ignore_order=True)
        self.assertEqual(diff, {})

if __name__ == '__main__':
    unittest.main()
