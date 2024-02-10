from threading import Lock
from channels.layers import get_channel_layer
import base64
from main import coordinator

class Singleton(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class WebsocketManager(metaclass=Singleton):
    def __init__(self):
        self.sessions = set()
        pass

    def add_session(self, session_id):
        self.sessions.add(session_id)

    def remove_session(self, session_id):
        coordinator.Coordinator().remove_node(session_id)
        self.sessions.remove(session_id)

    def get_connected_session_ids(self):
        return list(self.sessions)
    
    def is_node_alive(self, session_id):
        return session_id in self.sessions

    async def send_message_to_node(self, id, message):
        if id not in self.sessions:
            return False

        channel_layer = get_channel_layer()

        await channel_layer.group_send(
            id,
            {
                'type': 'send_message',
                'message': message,
            }
        )
        return True

    async def send_bytes_to_node(self, id, bytes_data):
        if not self.is_node_alive(id):
            return False
        channel_layer = get_channel_layer()

        await channel_layer.group_send(
            id,
            {
                'type': 'send_bytes',
                'bytes_data': bytes_data,
            }
        )
        return True
    

def b64_to_bytes(string: str) -> bytes:
    return base64.b64decode(string)


def bytes_to_b64(bytes_data: bytes) -> str:
    return base64.b64encode(bytes_data).decode('utf-8')