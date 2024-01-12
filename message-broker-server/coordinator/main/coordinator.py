from coordinator.websocket_manager import WebsocketManager
from coordinator.websocket_manager import Singleton
from models import *
import json


class Coordinator(metaclass=Singleton):
    def __init__(self):
        ip = '127.0.0.1'
        # todo: remove node

    def set_leader(self):
        leader = self.get_leader()
        if leader:
            leader.nodes = None
            leader.save()
        alive_nodes = self.get_alive_nodes()
        if alive_nodes:
            alive_nodes.update(is_leader=False)
            leader = alive_nodes.order_by('?').first()
            leader.is_leader = True
            leader.nodes = alive_nodes
            leader.save()
            self.notify_node(leader, {'type': 'became_leader', 'data': json.loads(leader.nodes)})

    def notify_node(self, node, message):
        id = node.id
        WebsocketManager.send_message_to_node(id, message)

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
        leader.add_node(node)
        return node
        # todo: notify leader

    def get_leader(self):
        return Node.objects.filter(is_leader=True).first()
    
    def get_alive_nodes(self):
        return Node.objects.filter(is_alive=True)
    
    def get_available_pair(self, ip):
        return Node.objects.filter(is_alive=True, pair=None).exclude(ip=ip).first()
