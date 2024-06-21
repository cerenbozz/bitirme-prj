import json
import os
import requests
from urllib.parse import urljoin
import threading
import time
from pynput import keyboard

general_counter = 0

# Define a function to perform the task
def perform_task():
    print("Performing the task...")
    api_token = "ENTER YOUR API TOKEN HERE"
    username = "isikkusgoz"
    pythonanywhere_host = "www.pythonanywhere.com"
    domain = "isikkusgoz.pythonanywhere.com"

    api_base = "https://{pythonanywhere_host}/api/v0/user/{username}/".format(
        pythonanywhere_host=pythonanywhere_host,
        username=username,
    )
    """resp = requests.post(
        urljoin(api_base, "webapps/{domain}/reload/".format(domain=domain)),
        headers={"Authorization": "Token {api_token}".format(api_token=api_token)}
    )
    if resp.status_code == 200:
    print('All OK')
    else:
    print('Got unexpected status code {}: {!r}'.format(resp.status_code, resp.content))
    """
    dir_files = [f for f in os.listdir("results")]
    for file in dir_files:
        dot_index = file.rfind('.')
        file_username = file[:dot_index] if dot_index != -1 else file
        file_extension = file[dot_index + 1:]
        if file_extension == "json":
            folder = "data"
            with open(f'results/{file}', 'r') as f:
                data = f.read()
            files = {"content": data}
        if file_extension == "png":
            folder = "static"
            files = {'content': open(f'results/{file}', 'rb')}

        global general_counter

        file = f"{file_username}_{general_counter}.{file_extension}"
        resp = requests.post(
            urljoin(api_base, f"files/path/home/{username}/mysite/{folder}/{file_username}/{file}"),
            files=files,
            headers={"Authorization": "Token {api_token}".format(api_token=api_token)}
        )
        print(file)
        print(resp.status_code)
        print(resp.content)


# This is the function that will run every 10 seconds
def periodic_task():
    global general_counter
    while not stop_event.is_set():
        perform_task()
        general_counter += 1
        general_counter %= 5
        time.sleep(10)

# This is the function that will run when the specific key is pressed
def on_press(key):
    global general_counter
    try:
        if key.char == 'q':  # Replace 'q' with your specific key
            print("Key pressed!")
            perform_task()
            general_counter += 1
            general_counter %= 5
    except AttributeError:
        pass

# Create a stop event for the loop
stop_event = threading.Event()

# Start the periodic task in a separate thread
thread = threading.Thread(target=periodic_task)
thread.start()

# Set up the key listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

try:
    # Keep the main thread running to listen for key presses
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Stop the loop if the user manually interrupts the script
    stop_event.set()
    thread.join()
    listener.stop()
    print("Program terminated.")
