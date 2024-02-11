from django.contrib import admin
from .models import *


class MessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Message._meta.get_fields()]

class ServerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Server._meta.get_fields()]

class NodeAdmin(admin.ModelAdmin):
    list_display = ['ip', 'port', 'is_alive', 'pair']
    # list_display = [field.name for field in Node._meta.get_fields()]

class NodeQueueAdmin(admin.ModelAdmin):
    list_display = [field.name for field in NodeQueue._meta.get_fields()]

admin.site.register(Message, MessageAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(NodeQueue, NodeQueueAdmin)
