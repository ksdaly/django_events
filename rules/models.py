import uuid
import sys

from abc import ABC, abstractmethod
from datetime import datetime

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.functional import cached_property


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

    def __str__(self):
        return ''.join(['%s: %s' % (prop, getattr(self, prop)) for prop in self.__slots__])

    __repr__ = __str__

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
    handler_type = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = JSONField()

    def __str__(self):
        return self.handler_type

    @cached_property
    def handler(self):
        return getattr(sys.modules[__name__], self.handler_type)(**self.data)
