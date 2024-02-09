import asyncio
import random
import json
import os

from channels.generic.websocket import AsyncWebsocketConsumer

from .websocket_manager import *

auth_cookie_name = os.getenv('WS_AUTH_COOKIE_NAME')


class WSConsumer(AsyncWebsocketConsumer):
    ping_interval: int = 10
    connected: bool
    session_id: int
    id: str

    async def connect(self):
        self.session_id = random.randint(0, 10000000000)
        self.id = str(self.scope['cookies']['id'])
        await self.channel_layer.group_add(self.id, self.channel_name)
        await self.accept()
        WebsocketManager().add_session(self.id)
        self.connected = True
        asyncio.create_task(self.schedule_ping())

    async def disconnect(self, close_code):
        self.connected = False
        await self.channel_layer.group_discard(self.id, self.channel_name)
        WebsocketManager().remove_session(self.id)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        pass

    async def send_message(self, message):
        to_send = {
            'type': 'message',
            'message': message
        }
        await self.send(text_data=to_send)

    async def send_bytes(self, bytes_data):
        to_send = bytes_to_b64(bytes_data)
        await self.send(text_data=to_send)

    async def schedule_ping(self):
        while True:
            await asyncio.sleep(self.ping_interval)
            if self.connected:
                await self.send(text_data=json.dumps({'type': 'ping'}))
            else:
                break