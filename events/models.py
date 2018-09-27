import uuid
import functools
import sys

from abc import ABC, abstractmethod
from datetime import datetime

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

class Base(ABC):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                pass

    @abstractmethod
    def is_eligible(self, data):
        pass

class Quantity(Base):
    __slots__ = ['qty']

    def is_eligible(self, data):
        return int(data['qty']) >= self.qty

class Category(Base):
    __slots__ = ['names']

    def is_eligible(self, data):
        return data['name'] in self.names

class DateTime(Base):
    __slots__ = ['_starts_at', '_ends_at']

    @property
    def starts_at(self):
        return self._starts_at

    @starts_at.setter
    def starts_at(self, value):
        self._starts_at = datetime.fromisoformat(value)

    @property
    def ends_at(self):
        return self._ends_at

    @ends_at.setter
    def ends_at(self, value):
        self._ends_at = datetime.fromisoformat(value)

    def is_eligible(self, data):
        return self.starts_at <= datetime.fromisoformat(data['occurred_at']) <= self.ends_at

class Rule(models.Model):
    type = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = JSONField()

    def __str__(self):
        return self.type

    @property
    @functools.lru_cache()
    def handler(self):
        return getattr(sys.modules[__name__], 'Quantity')(**self.data)

