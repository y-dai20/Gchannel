from asyncio import constants
from django.db import models
from django.conf import settings
from base.models import create_id
from base.models.functions import img_directory_path

class Room(models.Model):
    id = models.CharField(default=create_id, primary_key=True, max_length=settings.ID_LENGTH, editable=False)
    title = models.CharField(default='', max_length=255, blank=False)
    subtitle = models.CharField(default='', max_length=255, blank=False)
    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    img = models.ImageField(null=True, blank=True, upload_to=img_directory_path)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RoomGuest(models.Model):
    id = models.CharField(default=create_id, primary_key=True, max_length=settings.ID_LENGTH, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_allowed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['room', 'guest'], name="unique_stock")
        ]