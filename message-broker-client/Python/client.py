import json
import sys
import time
from threading import Thread, Lock

import requests

BASE_URL = 'http://127.0.0.1:8000/'
INTERVAL = 0.2
lock = Lock()


def pull():
    with lock:
        response = requests.post(BASE_URL + 'pull/')
        if response.text:
            message = response.json()
            return message['key'], message['value']
        return None, None


def push(key, value):
    message = json.dumps({'key': key, 'value': value})
    requests.post(BASE_URL + 'push/', data=message)


def subscribe(action):
    subscriber_thread = Thread(target=subscribe_thread, args=(action, INTERVAL))
    subscriber_thread.start()

def subscribe_thread(action, interval):
    while True:
        key, value = pull()
        if key:
            action(key, value)
        time.sleep(interval)
