from django.db import models


class Node(models.Model):
    ip = models.CharField(max_length=200)
    port = models.IntegerField(default=8000)
    is_leader = models.BooleanField(default=False)
    is_alive = models.BooleanField(default=True)
    pair = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.ip}:{self.port} - {self.id} - {self.is_alive}'
