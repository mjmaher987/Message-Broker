from django.http import HttpResponse
from .models import *
from .server import *
import json

from prometheus_client import Counter, Gauge, Histogram

# Prometheus metrics
total_nodes = Gauge('total_nodes', 'Total number of nodes')
message_size = Histogram('message_size_bytes', 'Size of messages in bytes')
push_counter = Counter('push_requests_total', 'Total number of push requests')
pull_counter = Counter('pull_requests_total', 'Total number of pull requests')


def message(request):
    message = json.loads(request.body)
    print(message)
    if message['type'] == 'became_leader':
        nodes = message['data']
        Server().is_leader = True
        Server().nodes = nodes
        total_nodes.set(len(nodes))  # for monitoring
        return HttpResponse(status=200)
    elif message['type'] == 'node_added':
        node = message['data']
        if not node in Server().nodes:
            Server().nodes.append(node)
            total_nodes.inc()  # for monitoring
        return HttpResponse(status=200)
    elif message['type'] == 'forward':
        message = message['data']
        message = Message.objects.create(key=message['key'], value=message['value'])
        message_size.observe(len(json.dumps(message_data)))  # for monitoring
        return HttpResponse(status=200)
    elif message['type'] == 'pull':
        pull_counter.inc()  # for monitoring
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
        push_counter.inc()  # for monitoring
        return HttpResponse(status=200)
    return HttpResponse(status=403)


def pull(request):
    if request.method == 'POST':
        message = Server().get_message()
        pull_counter.inc()  # for monitoring
        return HttpResponse(content=message, status=200)
    return HttpResponse(status=403)
