from django.http import HttpResponse
from .models import *
from .server import *
import json 

def message(request):
    message = request.POST
    if message['type'] == 'became_leader':
        nodes = message['data']
        Server().is_leader = True
        Server().nodes = nodes
        return HttpResponse(status=200)
    elif message['type'] == 'node_added':
        node = message['data']
        Server().nodes.append(node)
        return HttpResponse(status=200)
    elif message['type'] == 'forward':
        message = message['data']
        message = Message.objects.create(key=message['key'], value=message['value'])
        return HttpResponse(status=200)
    elif message['type'] == 'pull':
        message = Message.objects.filter(pulled=False).earliest('timestamp')
        message.pulled = True
        message.save()
        return HttpResponse(content=message, status=200)
    return HttpResponse(status=403)

def push(request):
    if request.method == 'POST':
        key = request.POST['key']
        value = request.POST['value']
        Server().forward_message({'key': key, 'value': value})
        return HttpResponse(status=200)
    return HttpResponse(status=403)

def pull(request):
    if request.method == 'POST':
        message = Server().get_message()
        return HttpResponse(content=message, status=200)
    return HttpResponse(status=403)

        