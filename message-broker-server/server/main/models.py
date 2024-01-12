from django.db import models
    

class Message(models.Model):
    key = models.CharField(max_length=200)
    value = models.BinaryField()
    pulled = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

