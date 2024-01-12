from django.shortcuts import render
from models import *
from server import *
from django.http import HttpResponse


def became_leader(request):
    if request.method == 'POST':
        #  = request.data
        Server().is_leader = True
        return HttpResponse(status=200)
    return HttpResponse(status=403)

def push(request):
    if request.method == 'POST':
        key = request.POST['key']
        value = request.POST['value']

        server = Server()
        