from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Sms


@receiver(post_save, sender=User)
def send_pickup_sms(sender, instance=None, created=False, **kwargs):
    if created:
        Sms.objects.send_sms(instance.mobile, 'register_sucess')
