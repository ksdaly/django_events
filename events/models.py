import uuid

from datetime import datetime

from django.db import models
from django.contrib.postgres.fields import JSONField

from rules.models import Rule


class Event(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(auto_now=False, null=True)
    data = JSONField()

    def __str__(self):
        return str(self.message_id)

    def process(self):
        self.is_eligible()
        self.processed()

    def processed(self):
        self.processed_at = datetime.now()
        self.save()

    def is_eligible(self):
        for rule in Rule.objects.all():
            if not rule.handler.is_eligible(self.data):
                return False
        return True
