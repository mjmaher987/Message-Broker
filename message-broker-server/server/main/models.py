from django.db import models
    

class Message(models.Model):
    node = models.ForeignKey(Server, on_delete=models.SET_NULL)
    key = models.CharField(max_length=200)
    value = models.BinaryField()
    timestamp = models.DateTimeField(auto_now_add=True)

