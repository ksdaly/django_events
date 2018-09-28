import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Rule, Quantity, Category, DateTime

def create_rule(props=None):
    """
    Create a rule
    """
    defaults = {
        'handler_type': 'Quantity',
        'data': {
            'qty': 1
        }
    }

    if props: defaults.update(props)

    return Rule.objects.create(**defaults)

class RuleModelTests(TestCase):

    def test_was_created(self):
        """
        Create a rule
        """
        rule = create_rule()
        self.assertTrue(
            Rule.objects.filter(pk = rule.pk).exists()
        )

    def test_has_handler(self):
        """
        Initializes and caches handler property for specified handler with rule data
        """
        rule = create_rule()
        self.assertIsInstance(rule.handler, Quantity)
        self.assertEqual(rule.handler.qty, rule.data['qty'])
        self.assertIs(rule.handler, rule.handler)

class QuantityTests(TestCase):

    def test_is_eligible(self):
        handler = Quantity(**{'qty': 1})
        event = {
            'qty': 1,
            'name': 'Coffee',
            'amount': 199,
            'occurred_at': datetime.datetime.now().isoformat()
        }

        self.assertTrue(
            handler.is_eligible(event)
        )

    def test_is_not_eligible(self):
        handler = Quantity(**{'qty': 2})
        event = {
            'qty': 1,
            'name': 'Coffee',
            'amount': 199,
            'occurred_at': datetime.datetime.now().isoformat()
        }

        self.assertFalse(
            handler.is_eligible(event)
        )

class CategoryTests(TestCase):

    def test_is_eligible(self):
        handler = Category(**{'names': 'Coffee'})
        event = {
            'qty': 1,
            'name': 'Coffee',
            'amount': 199,
            'occurred_at': datetime.datetime.now().isoformat()
        }

        self.assertTrue(
            handler.is_eligible(event)
        )

    def test_is_not_eligible(self):
        handler = Category(**{'names': 'Bagel'})
        event = {
            'qty': 1,
            'name': 'Coffee',
            'amount': 199,
            'occurred_at': datetime.datetime.now().isoformat()
        }

        self.assertFalse(
            handler.is_eligible(event)
        )

class DateTimeTests(TestCase):

    def test_is_eligible(self):
        now = datetime.datetime.now()
        starts_at = now - datetime.timedelta(days=1)
        ends_at = now + datetime.timedelta(days=1)
        handler = DateTime(**{'starts_at': starts_at.isoformat(), 'ends_at': ends_at.isoformat()})
        event = {
            'qty': 1,
            'name': 'Coffee',
            'amount': 199,
            'occurred_at': now.isoformat()
        }

        self.assertTrue(
            handler.is_eligible(event)
        )

    def test_is_not_eligible(self):
        now = datetime.datetime.now()
        starts_at = now - datetime.timedelta(days=1)
        ends_at = now + datetime.timedelta(days=1)
        handler = DateTime(**{'starts_at': starts_at.isoformat(), 'ends_at': ends_at.isoformat()})
        event = {
            'qty': 1,
            'name': 'Coffee',
            'amount': 199,
            'occurred_at': (ends_at + datetime.timedelta(days=1)).isoformat()
        }

        self.assertFalse(
            handler.is_eligible(event)
        )
