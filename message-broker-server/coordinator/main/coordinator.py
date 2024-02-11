from coordinator.websocket_manager import WebsocketManager
from coordinator.websocket_manager import Singleton
from django.conf import settings
from .models import *
import requests
from asgiref.sync import sync_to_async

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()


class Coordinator(metaclass=Singleton):
    def __init__(self):
        self.ip = '127.0.0.1'
        self.nodes_removed = 0

    def set_leader(self):
        leader = self.get_leader()
        alive_nodes = self.get_alive_nodes()
        if alive_nodes:
            alive_nodes.update(is_leader=False)
            leader = alive_nodes.order_by('?').first()
            leader.is_leader = True
            leader.save()
            self.notify_node(leader, {'type': 'became_leader', 'data': [(node.ip, node.port) for node in alive_nodes], 'port': leader.port})

    def notify_node(self, node, message):
        # id = node.id
        # WebsocketManager.send_message_to_node(id, message)
        requests.post(f'http://{node.ip}:{node.port}/message/', json=message)

    def add_node(self, ip):
        port = int(settings.NODE_PORT) + self.get_alive_nodes().count() + self.nodes_removed
        node, _ = Node.objects.get_or_create(ip=ip, port=port)
        node.is_alive = True
        pair = self.get_available_pair(ip, port)
        if pair:
            node.pair = pair
            pair.pair = node
            pair.save()
        node.save()
        leader = self.get_leader()
        if not leader:
            self.set_leader()
            leader = self.get_leader()
        if pair:
            self.notify_node(leader, {'type': 'node_added', 'data': {'node': (node.ip, node.port), 'pair': (pair.ip, pair.port)}})
        else:
            self.notify_node(leader, {'type': 'node_added', 'data': {'node': (node.ip, node.port)}})
        return node
    
    def remove_node(self, id):
        node = Node.objects.filter(id=id).first()
        if node:
            leader = self.get_leader()
            self.notify_node(leader, {'type': 'node_removed', 'data': {'node': (node.ip, node.port)}})
            node.is_alive = False
            if node.pair:
                node.pair.pair = None
                node.pair.save()
                node.pair = None
            node.save()
            self.nodes_removed += 1

    def get_leader(self):
        return Node.objects.filter(is_leader=True, is_alive=True).first()
    
    def get_alive_nodes(self):
        return Node.objects.filter(is_alive=True)
    
    def get_available_pair(self, ip, port):
        return Node.objects.filter(is_alive=True, pair=None).exclude(ip=ip, port=port).first()
