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
        self.port = ''
        self.is_leader = False
        self.nodes = []
        self.pair = None
        self.nodes_queue = queue.Queue()

    def forward_message(self, message):
        if not self.is_leader:
            return
        key_hash = hashlib.sha256(message['key'].encode()).digest()
        nodes = sorted(self.nodes)
        (node_ip, node_port) = nodes[key_hash[0] % len(nodes)]
        if node_port == self.port:
            Message.objects.create(key=message['key'], value=message['value'].encode())
            self.nodes_queue.put((node_ip, node_port))
        else:
            response = requests.post(f'http://{node_ip}:{node_port}/message/',
                                    data=json.dumps({'type': 'forward', 'data': message}))
            if response.status_code == 200:
                self.nodes_queue.put((node_ip, node_port))

    def get_message(self):
        if not self.is_leader:
            return None

        (node_ip, node_port) = self.nodes_queue.get()
        if node_port == self.port:
            message = Message.objects.filter(pulled=False).earliest('timestamp')
            message.pulled = True
            message.save()
            print(message)
            return {'key': message.key, 'value': message.value}
        else:
            response = requests.post(f'http://{node_ip}:{node_port}/message/', data=json.dumps({'type': 'pull'}))
            return response.json()