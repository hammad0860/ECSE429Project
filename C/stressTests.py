import subprocess
import requests
import os
import time
import csv
import psutil
import threading
import matplotlib.pyplot as plt
import pandas as pd
from dataGenerator import generateTodo
from requestClient import createTodo, updateTodo, deleteTodo

BASE_URL = "http://localhost:4567"
TODO_URL = f"{BASE_URL}/todos"

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
CSV_DIR = os.path.join(SCRIPT_DIR, "csv")
GRAPH_DIR = os.path.join(SCRIPT_DIR, "graphs")
WORKING_DIRECTORY = os.path.abspath(os.path.join(SCRIPT_DIR, "../"))
APP_PROCESS = None

def start_app():
    global APP_PROCESS
    print("Starting the Application")
    APP_PROCESS = subprocess.Popen(
        ["java", "-jar", os.path.join(WORKING_DIRECTORY, "runTodoManagerRestAPI-1.5.5.jar")],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=WORKING_DIRECTORY,
        shell=True
    )
    wait_for_server()

def wait_for_server():
    while True:
        try:
            response = requests.get(TODO_URL, timeout=3)
            if response.status_code == 200:
                break
        except:
            pass
        time.sleep(1)

def shutdown_app():
    print("Shutting down Application")
    global APP_PROCESS
    try:
        requests.get(f"{BASE_URL}/shutdown")
    except:
        pass
    if APP_PROCESS:
        APP_PROCESS.terminate()
        APP_PROCESS.wait()

def monitor_resources(sample_interval, duration, output_file):
    end_time = time.time() + duration
    f = open(output_file, 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(["Sample Time (ms)", "CPU Usage (%)", "Free Memory (MB)"])
    start_time = time.time()
    while time.time() < end_time:
        current_time = time.time()
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().available / (1024 * 1024)
        elapsed = int((current_time - start_time) * 1000)
        writer.writerow([elapsed, cpu, mem])
        time.sleep(sample_interval)
    f.close()

def run_stress_test():
    sizes = [100, 200, 300, 500, 1000, 3000, 5000]
    results = []
    print("Starting stress tests...")
    for n in sizes:
        ids = []
        duration = n * 0.01
        print(f"Running create for {n} items...")
        monitor_thread = threading.Thread(
            target=monitor_resources,
            args=(0.1, duration, os.path.join(CSV_DIR, f"create_for_{n}.csv"))
        )
        monitor_thread.start()
        start = time.time()
        for _ in range(n):
            todo = generateTodo()
            res = createTodo(todo)
            if res.ok:
                ids.append(res.json().get("id"))
        create_time = time.time() - start
        monitor_thread.join()

        print(f"Running update for {n} items...")
        monitor_thread = threading.Thread(
            target=monitor_resources,
            args=(0.1, duration, os.path.join(CSV_DIR, f"update_for_{n}.csv"))
        )
        monitor_thread.start()
        start = time.time()
        for id in ids:
            updateTodo(id, {"doneStatus": True})
        update_time = time.time() - start
        monitor_thread.join()

        print(f"Running delete for {n} items...")
        monitor_thread = threading.Thread(
            target=monitor_resources,
            args=(0.1, duration, os.path.join(CSV_DIR, f"delete_for_{n}.csv"))
        )
        monitor_thread.start()
        start = time.time()
        for id in ids:
            deleteTodo(id)
        delete_time = time.time() - start
        monitor_thread.join()

        results.append([n, create_time / n, update_time / n, delete_time / n])
        print(f"Completed stress test for {n} items.")

    f = open(os.path.join(CSV_DIR, "stress_results.csv"), "w", newline='')
    writer = csv.writer(f)
    writer.writerow(["Num_Items", "Create_Time", "Update_Time", "Delete_Time"])
    writer.writerows(results)
    f.close()
    print("Stress tests completed.")

def plot_metrics():
    sizes = [100, 200, 300, 500, 1000, 3000, 5000]
    stress_df = pd.read_csv(os.path.join(CSV_DIR, "stress_results.csv"))
    avg_cpu = {"Create": [], "Update": [], "Delete": []}
    avg_mem = {"Create": [], "Update": [], "Delete": []}

    for n in sizes:
        create_df = pd.read_csv(os.path.join(CSV_DIR, f"create_for_{n}.csv"))
        update_df = pd.read_csv(os.path.join(CSV_DIR, f"update_for_{n}.csv"))
        delete_df = pd.read_csv(os.path.join(CSV_DIR, f"delete_for_{n}.csv"))

        avg_cpu["Create"].append(create_df["CPU Usage (%)"].mean())
        avg_cpu["Update"].append(update_df["CPU Usage (%)"].mean())
        avg_cpu["Delete"].append(delete_df["CPU Usage (%)"].mean())

        avg_mem["Create"].append(create_df["Free Memory (MB)"].mean())
        avg_mem["Update"].append(update_df["Free Memory (MB)"].mean())
        avg_mem["Delete"].append(delete_df["Free Memory (MB)"].mean())

    os.makedirs(GRAPH_DIR, exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.plot(sizes, avg_cpu["Create"], label="Create", marker="o")
    plt.plot(sizes, avg_cpu["Update"], label="Update", marker="o")
    plt.plot(sizes, avg_cpu["Delete"], label="Delete", marker="o")
    plt.xlabel("Number of TODOs")
    plt.ylabel("Average CPU Usage (%)")
    plt.title("Average CPU Usage vs Number of TODOs")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR, "cpu_vs_num_todos.png"))
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(sizes, avg_mem["Create"], label="Create", marker="o")
    plt.plot(sizes, avg_mem["Update"], label="Update", marker="o")
    plt.plot(sizes, avg_mem["Delete"], label="Delete", marker="o")
    plt.xlabel("Number of TODOs")
    plt.ylabel("Average Free Memory (MB)")
    plt.title("Average Free Memory vs Number of TODOs")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR, "memory_vs_num_todos.png"))
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(stress_df["Num_Items"], stress_df["Create_Time"], marker="o", label="Create Time per TODO")
    plt.plot(stress_df["Num_Items"], stress_df["Update_Time"], marker="o", label="Update Time per TODO")
    plt.plot(stress_df["Num_Items"], stress_df["Delete_Time"], marker="o", label="Delete Time per TODO")
    plt.xlabel("Number of TODOs")
    plt.ylabel("Time per TODO (s)")
    plt.title("Transaction Time per TODO vs Number of TODOs")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR, "transaction_time_per_todo_vs_num_todos.png"))
    plt.close()

if __name__ == "__main__":
    os.makedirs(CSV_DIR, exist_ok=True)
    os.makedirs(GRAPH_DIR, exist_ok=True)
    start_app()
    try:
        run_stress_test()
    finally:
        shutdown_app()
        plot_metrics()
