from threading import Lock
from models import Message
import hashlib


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

    def forward_message(self, message: Message):
        if not self.is_leader:
            return
        key_hash = hashlib.sha256(message.key.encode()).digest()
        nodes = self.nodes.all().order_by('ip')
        node = nodes[key_hash[0] % len(nodes)]
        
        # todo: send message