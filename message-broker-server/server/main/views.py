from django.http import HttpResponse
from .models import *
import json

def message(request):
    message = json.loads(request.body)
    print(message)
    if message['type'] == 'became_leader':
        nodes = message['data']
        port = message['port']
        Server.objects.all().update(is_leader=False)
        server, _ = Server.objects.get_or_create(port=port)
        server.is_leader = True
        server.save()
        for node in nodes:
            Node.objects.get_or_create(ip=node[0], port=node[1])
        return HttpResponse(status=200)
    elif message['type'] == 'node_added':
        data = message['data']
        node, _ = Node.objects.get_or_create(ip=data['node'][0], port=data['node'][1])
        if 'pair' in data:
            pair, _ = Node.objects.get_or_create(ip=data['pair'][0], port=data['pair'][1])
            node.pair = pair
            pair.pair = node
            node.save()
            pair.save()
        return HttpResponse(status=200)
    elif message['type'] == 'node_removed':
        data = message['data']
        node = Node.objects.get(ip=data['node'][0], port=data['node'][1])
        node.is_alive = False
        if node.pair:
            node.pair.pair = None
            node.pair.save()
        node.save()
        return HttpResponse(status=200)
    elif message['type'] == 'forward':
        message = message['data']
        Message.objects.create(key=message['key'], value=message['value'].encode())
        return HttpResponse(status=200)
    elif message['type'] == 'forward_replica':
        message = message['data']
        Message.objects.create(key=message['key'], value=message['value'].encode(), is_replica=True)
        return HttpResponse(status=200)
    elif message['type'] == 'pull':
        message = Message.objects.filter(pulled=False, is_replica=False).earliest('timestamp')
        message.pulled = True
        message.save()
        return HttpResponse(content=json.dumps({'key': message.key, 'value': message.value.decode()}), status=200)
    elif message['type'] == 'pull_replica':
        message = Message.objects.filter(pulled=False, is_replica=True).earliest('timestamp')
        message.pulled = True
        message.save()
        return HttpResponse(content=json.dumps({'key': message.key, 'value': message.value.decode()}), status=200)
    return HttpResponse(status=403)

def push(request):
    if request.method == 'POST':
        server = Server.objects.filter(is_leader=True).first()
        message = json.loads(request.body)
        key = message['key']
        value = message['value']
        server.forward_message({'key': key, 'value': value})
        return HttpResponse(status=200)
    return HttpResponse(status=403)

def pull(request):
    if request.method == 'POST':
        server = Server.objects.filter(is_leader=True).first()
        message = server.get_message()
        if message:
            return HttpResponse(content=json.dumps(message), status=200)
        else:
            return HttpResponse(status=200)
    return HttpResponse(status=403)

