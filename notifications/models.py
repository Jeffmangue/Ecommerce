from enum import unique
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group


class NotificationsModel(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_message', blank=True,null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages',blank=True,null=True)
    subject = models.CharField(max_length=500,null=True,blank=True)
    body = models.TextField(null=True,blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True,null=True)
    admin_feedback = models.CharField(max_length=500,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    def __str__(self):
        return str(self.sender)

