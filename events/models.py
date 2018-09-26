import datetime
import uuid

from abc import ABC

from django.db import models
from django.contrib.postgres.fields import JSONField


class Event(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(auto_now=False, null=True)
    data = JSONField()

    def __str__(self):
        return str(self.message_id)

class Rule(models.Model):
    type = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = JSONField()

    def __str__(self):
        return self.type

class Base(ABC):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                pass

class Quantity(Base):
    __slots__ = ['qty']

    def is_eligible(self, data):
        return self.qty <= int(data['qty'])

