from django.shortcuts import render
from coordinator.websocket_manager import WebsocketManager
from coordinator import Coordinator
from django.http import HttpResponse


def connect(request):
    if request.method == 'POST':
        ip = request.META.get('REMOTE_ADDR')
        node = Coordinator().add_node(ip)
        return HttpResponse(content=node.id, status=200)
    return HttpResponse(status=403)