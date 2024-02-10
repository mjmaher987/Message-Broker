from django.contrib import admin
from .models import *


class NodeAdmin(admin.ModelAdmin):
    list_display = ['ip', 'is_leader', 'is_alive', 'pair', 'port']
    # list_display = [field.name for field in Node._meta.get_fields()]


admin.site.register(Node, NodeAdmin)
