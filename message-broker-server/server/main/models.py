from django.db import models
import requests
import hashlib
import json


class Message(models.Model):
    key = models.CharField(max_length=200)
    value = models.BinaryField()
    is_replica = models.BooleanField(default=False)
    pulled = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class Node(models.Model):
    ip = models.CharField(max_length=200, default='127.0.0.1')
    port = models.IntegerField(default=8000)
    is_alive = models.BooleanField(default=True)
    pair = models.ForeignKey('Node', on_delete=models.SET_NULL, null=True)

class NodeQueue(models.Model):
    ip = models.CharField(max_length=200)
    port = models.IntegerField(default=8000)

class Server(models.Model):
    port = models.IntegerField(default=8000)
    is_leader = models.BooleanField(default=False)

    def forward_message(self, message):
        if not self.is_leader:
            return
        key_hash = hashlib.sha256(message['key'].encode()).digest()
        nodes = Node.objects.all().order_by('id')
        node = nodes[key_hash[0] % len(nodes)]
        if node.port == self.port:
            Message.objects.create(key=message['key'], value=message['value'].encode())
            requests.post(f'http://{node.pair.ip}:{node.pair.port}/message/',
                                     data=json.dumps({'type': 'forward_replica', 'data': message}))
            NodeQueue.objects.create(ip=node.ip, port=node.port)
        else:
            response = requests.post(f'http://{node.ip}:{node.port}/message/',
                                     data=json.dumps({'type': 'forward', 'data': message}))
            requests.post(f'http://{node.pair.ip}:{node.pair.port}/message/',
                                     data=json.dumps({'type': 'forward_replica', 'data': message}))
            if response.status_code == 200:
                NodeQueue.objects.create(ip=node.ip, port=node.port)

    def get_message(self):
        if not self.is_leader:
            return None

        node = NodeQueue.objects.first()
        if node:
            node_ip, node_port = node.ip, node.port
            real_node = Node.objects.get(ip=node_ip, port=node_port)
            node_pair_ip, node_pair_port = real_node.pair.ip, real_node.pair.port
            node.delete()
            if real_node.is_alive:
                if node_port == self.port:
                    message = Message.objects.filter(pulled=False).earliest('timestamp')
                    message.pulled = True
                    message.save()
                    return {'key': message.key, 'value': message.value.decode()}
                else:
                    response = requests.post(f'http://{node_ip}:{node_port}/message/', data=json.dumps({'type': 'pull'}))
                    requests.post(f'http://{node_pair_ip}:{node_pair_port}/message/', data=json.dumps({'type': 'pull_replica'}))
                    return response.json()
            else:
                response = requests.post(f'http://{node_pair_ip}:{node_pair_port}/message/', data=json.dumps({'type': 'pull_replica'}))
                return response.json()
        else:
            return None

