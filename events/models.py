import datetime
import uuid

from django.db import models
from django.contrib.postgres.fields import JSONField


class Event(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    data = JSONField()

    def __str__(self):
        return str(self.message_id)
