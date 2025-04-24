from django.contrib.auth.models import User
from django.db import models
import socket

def get_ip():
    return socket.gethostbyname(socket.gethostname())

class EmailLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    encrypted_message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    sender_ip = models.GenericIPAddressField(default=get_ip)
    file_attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    bandwidth_used = models.FloatField(default=0.0)
