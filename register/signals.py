from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from datetime import datetime
from notifications.models import NotificationsModel


# @receiver(post_save, sender=User)
# def send_notif_to_admin(sender, instance, created, **kwargs):
#     superusers = User.objects.filter(is_superuser=True)
#     for user in superusers:
#         nt = NotificationsModel(sender=instance.user,receiver=user)
#         nt.save()


