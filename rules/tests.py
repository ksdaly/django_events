import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Rule, Quantity

def create_rule(props=None):
    """
    Create a rule
    """
    defaults = {
        'handler_type': 'Quantity',
        'data': {
            'qty': 1,
            'name': 'Coffee',
            'amount': 199,
            'occurred_at': datetime.datetime.now().isoformat()
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
