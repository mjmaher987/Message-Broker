from .coordinator import Coordinator
from django.http import HttpResponse


coordinator = Coordinator()

def connect(request):
    if request.method == 'POST':
        ip = request.META.get('REMOTE_ADDR')
        node = coordinator.add_node(ip)
        return HttpResponse(content=node.id, status=200)
    return HttpResponse(status=403)