from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.subscriptions.models import Plan
from apps.billing.models import Subscription
from tenants.models import Tenant

User=get_user_model()

class SubscriptionStateTest(TestCase):

    def setUp(self):
        self.user=User.objects.create_user(
            email="test@test.com",
            password="testpass"
        )

        self.plan=Plan.objects.create(
            name="Basic",
            price=10,
            duration_days=30,
            quota=100
        )

        self.tenant=Tenant.objects.create(
            name="Test Org",
            owner=self.user
        )

    def test_default_subscription_state(self):
        subscription=Subscription.objects.create(
            tenant=self.tenant,
            plan=self.plan
        )

        self.assertTrue(subscription.is_active) # default =True
        self.assertFalse(subscription.is_trial)  #default=False