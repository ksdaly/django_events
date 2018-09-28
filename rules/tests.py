import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Rule

def create_rule(data=None):
    """
    Create a rule
    """
    defaults = {
        'qty': 1,
        'name': 'Coffee',
        'amount': 199,
        'occurred_at': datetime.datetime.now().isoformat()
    }

    if data: defaults.update(data)

    return Rule.objects.create(data=defaults)

class RuleModelTests(TestCase):

    def test_was_created(self):
        """
        create a rule
        """
        rule = create_rule()
        self.assertTrue(
            Rule.objects.filter(pk = rule.pk).exists()
        )
