from coordinator.websocket_manager import WebsocketManager
from coordinator.websocket_manager import Singleton
from django.conf import settings
from .models import *
import requests
import json


class Coordinator(metaclass=Singleton):
    def __init__(self):
        self.ip = '127.0.0.1'
        # todo: remove node

    def set_leader(self):
        leader = self.get_leader()
        alive_nodes = self.get_alive_nodes()
        if alive_nodes:
            alive_nodes.update(is_leader=False)
            leader = alive_nodes.order_by('?').first()
            leader.is_leader = True
            leader.save()
            self.notify_node(leader, {'type': 'became_leader', 'data': [node.ip for node in alive_nodes]})

    def notify_node(self, node, message):
        # id = node.id
        # WebsocketManager.send_message_to_node(id, message)
        requests.post(f'http://{node.ip}:{settings.NODE_PORT}/message/', data=message)
        

    def add_node(self, ip):
        node, created = Node.objects.get_or_create(ip=ip)
        pair = self.get_available_pair(ip)
        if pair:
            node.pair = pair
            pair.pair = node
            pair.save()
            node.save()
        leader = self.get_leader()
        if not leader:
            self.set_leader()
            leader = self.get_leader()
        self.notify_node(leader, {'type': 'node_added', 'data': ip})
        return node

    def get_leader(self):
        return Node.objects.filter(is_leader=True).first()
    
    def get_alive_nodes(self):
        return Node.objects.filter(is_alive=True)
    
    def get_available_pair(self, ip):
        return Node.objects.filter(is_alive=True, pair=None).exclude(ip=ip).first()
