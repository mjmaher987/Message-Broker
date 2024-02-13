from django.http import HttpResponse
from .models import *
import json
from threading import Lock

from prometheus_client import Counter, Gauge, Histogram

# Prometheus metrics
total_nodes = Gauge('total_nodes', 'Total number of nodes')
message_size = Histogram('message_size_bytes', 'Size of messages in bytes')
push_counter = Counter('push_requests_total', 'Total number of push requests')
pull_counter = Counter('pull_requests_total', 'Total number of pull requests')


lock = Lock()

def message(request):
    message = json.loads(request.body)
    # print(message)
    if message['type'] == 'became_leader':
        nodes = message['data']
        port = message['port']
        Server.objects.all().update(is_leader=False)
        server, _ = Server.objects.get_or_create(port=port)
        server.is_leader = True
        server.save()
        total_nodes.set(len(nodes)) # monitoring
        for node in nodes:
            Node.objects.get_or_create(ip=node[0], port=node[1])
        return HttpResponse(status=200)
    elif message['type'] == 'node_added':
        with lock:
            data = message['data']
            node, _ = Node.objects.get_or_create(ip=data['node'][0], port=data['node'][1])
            total_nodes.inc()  # for monitoring
            if 'pair' in data:
                pair, _ = Node.objects.get_or_create(ip=data['pair'][0], port=data['pair'][1])
                node.pair = pair
                pair.pair = node
                node.save()
                pair.save()
            return HttpResponse(status=200)
    elif message['type'] == 'node_removed':
        with lock:
            data = message['data']
            node = Node.objects.get(ip=data['node'][0], port=data['node'][1])
            node.is_alive = False
            total_nodes.dec()  # for monitoring
            if node.pair:
                node.pair.pair = None
                node.pair.save()
            node.save()
            return HttpResponse(status=200)
    elif message['type'] == 'forward':
        message = message['data']
        Message.objects.create(key=str(message['key']), value=message['value'].encode())
        message_size.observe(len(json.dumps(message)))  # for monitoring
        return HttpResponse(status=200)
    elif message['type'] == 'forward_replica':
        message = message['data']
        Message.objects.create(key=str(message['key']), value=message['value'].encode(), is_replica=True)
        return HttpResponse(status=200)
    elif message['type'] == 'pull':
        pull_counter.inc()  # for monitoring
        message = Message.objects.filter(pulled=False, is_replica=False).earliest('timestamp')
        message.pulled = True
        message.save()
        return HttpResponse(content=json.dumps({'key': str(message.key), 'value': message.value.decode()}), status=200)
    elif message['type'] == 'pull_replica':
        message = Message.objects.filter(pulled=False, is_replica=True).earliest('timestamp')
        message.pulled = True
        message.save()
        return HttpResponse(content=json.dumps({'key': str(message.key), 'value': message.value.decode()}), status=200)
    return HttpResponse(status=403)

def push(request):
    if request.method == 'POST':
        with lock:
            server = Server.objects.filter(is_leader=True).first()
            message = json.loads(request.body)
            key = str(message['key'])
            value = message['value']
            server.forward_message({'key': key, 'value': value})
            push_counter.inc()  # for monitoring
            return HttpResponse(status=200)
    return HttpResponse(status=403)

def pull(request):
    if request.method == 'POST':
        with lock:
            pull_counter.inc()  # for monitoring
            server = Server.objects.filter(is_leader=True).first()
            message = server.get_message()
            if message:
                return HttpResponse(content=json.dumps(message), status=200)
            else:
                return HttpResponse(status=200)
    return HttpResponse(status=403)

