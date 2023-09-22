import subprocess
import os
import time
import threading
import sys
import gradio

print("Running this is not reccomended as it is in development and will not work as expected.")
time.sleep(5)

# Shared variable to signal a UI reload
reload_requested = False
reload_lock = threading.Lock()

# Function to restart the UI
def restart_ui():
    # Start a new UI process with stdin, stdout, and stderr connected to the current process
    subprocess.Popen([sys.executable, "ui.py"], stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)

# Start the UI as a separate process
ui_process = subprocess.Popen([sys.executable, "ui.py"], stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr)

def reload_listener():
    global reload_requested
    while True:
        if reload_requested:
            # Restart the UI process and keep stdin, stdout, and stderr connected
            ui_process.terminate()
            ui_process.wait()
            time.sleep(5)
            gradio.close_all()
            restart_ui()
            reload_requested = False
        time.sleep(1)

# Start a thread to listen for reload requests
reload_thread = threading.Thread(target=reload_listener)
reload_thread.daemon = True
reload_thread.start()

while True:
    user_input = input("Enter 'exit' to exit: ")
    if user_input == "exit":
        # Terminate the UI process and exit the script
        ui_process.terminate()
        ui_process.wait()
        break
