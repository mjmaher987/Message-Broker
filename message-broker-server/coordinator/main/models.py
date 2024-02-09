from django.db import models


class Node(models.Model):
    ip = models.CharField(max_length=200)
    is_leader = models.BooleanField(default=False)
    is_alive = models.BooleanField(default=True)
    pair = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.ip}: {self.is_alive}'
