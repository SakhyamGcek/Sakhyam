from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def activate_user(sender, instance, **kwargs):
    if instance.is_approved and not instance.is_active:
        instance.is_active = True
        instance.save()
