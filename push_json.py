import json

import requests
import requests
from urllib.parse import urljoin


import threading
import time
from pynput import keyboard

# Define a function to perform the task
def perform_task():
    print("Performing the task...")
    api_token = "1d52d143451da56520e8e5f982237d7dbfc3c230"
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
    with open('emotion_results.json', 'r') as file:
        data = file.read()
    files = {"content": data}
    resp = requests.post(
        urljoin(api_base, "files/path/home/{username}/mysite/emotion_results.json".format(username=username)),
        files=files,
        headers={"Authorization": "Token {api_token}".format(api_token=api_token)}
    )
    print(resp.status_code)
    print(resp.content)

# This is the function that will run every 10 seconds
def periodic_task():
    while not stop_event.is_set():
        perform_task()
        time.sleep(10)

# This is the function that will run when the specific key is pressed
def on_press(key):
    try:
        if key.char == 'q':  # Replace 'q' with your specific key
            print("Key pressed!")
            perform_task()
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
