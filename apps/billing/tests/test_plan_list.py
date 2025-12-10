from django.test import TestCase
from rest_framework.test import APIClient
from apps.subscriptions.models import Plan


class PlanListTest(TestCase):
    def setUp(self):
        self.client=APIClient()
        Plan.objects.create(
            name="Basic",
            price=10,
            duration_days=30,
            quota=100
        )
        Plan.objects.create(
            name="Pro",
            price=20,
            duration_days=30,
            quota=200
        )


    def test_plan_list(self):
        response =self.client.get("/api/plans/")

        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),2)
        # self.assertEqual(response.data[0]["name"],"Basic")

