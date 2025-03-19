import requests
import subprocess
import os
import time

BASE_URL = "http://localhost:4567"
WORKING_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", ".."))
APPLICATION_PROCESS = None

def start_application():
    global APPLICATION_PROCESS
    jar_path = os.path.join(WORKING_DIR, "runTodoManagerRestAPI-1.5.5.jar")
    APPLICATION_PROCESS = subprocess.Popen(
        ["java", "-jar", jar_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=WORKING_DIR,
        shell=True
    )
    wait_for_server()

def stop_application():
    global APPLICATION_PROCESS
    try:
        requests.get(f"{BASE_URL}/shutdown", timeout=3)
    except requests.exceptions.RequestException:
        pass
    APPLICATION_PROCESS.terminate()

def wait_for_server():
    for _ in range(10):
        try:
            response = requests.get(f"{BASE_URL}/todos", timeout=2)
            if response.status_code == 200:
                return
        except requests.exceptions.RequestException:
            pass
    raise RuntimeError("Server did not start in time.")

def before_scenario(context, scenario):
    start_application()


def after_scenario(context, scenario):
    stop_application()
