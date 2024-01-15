from django.conf import settings
from threading import Lock
from .models import Message
import requests
import hashlib
import json
import queue


class Singleton(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Server(metaclass=Singleton):
    def __init__(self):
        self.ip = '127.0.0.1'
        self.is_leader = False
        self.nodes = []
        self.pair = None
        self.nodes_queue = queue.Queue()

    def forward_message(self, message):
        if not self.is_leader:
            return
        key_hash = hashlib.sha256(message['key'].encode()).digest()
        nodes = sorted(self.nodes)
        node_ip = nodes[key_hash[0] % len(nodes)]
        response = requests.post(f'http://{node_ip}:{settings.NODE_PORT}/message', data=json.dumps({'type': 'forward', 'data': message}))
        if response.status_code == 200:
            self.nodes_queue.put(node_ip)

    def get_message(self):
        if not self.is_leader:
            return None
        
        node_ip = self.nodes_queue.get()
        response = requests.post(f'http://{node_ip}:{settings.NODE_PORT}/message', data=json.dumps({'type': 'pull'}))
        return response.content