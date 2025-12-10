from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from tenants.models import Tenant

User=get_user_model()

class TenantCreationTest(TestCase):
    def setUp(self):
        self.client=APIClient()
        self.user=User.objects.create_user(
            email="test@test.com",
            password="testpass"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_tenant(self):
        payload={
            "name":"Test Org"
        }

        response = self.client.post("/api/tenants/create/",payload,format="json")

        self.assertEqual(response.status_code,201)
        self.assertEqual(Tenant.objects.count(),1)

        tenant=Tenant.objects.first()
        self.assertEqual(tenant.name,"Test Org")
        self.assertEqual(tenant.owner,self.user)

    def test_create_tenant_without_name(self):
        payload={

        }

        response=self.client.post("/api/tenants/create/",payload,format="json")

        self.assertEqual(response.status_code,400)
        self.assertIn('name',response.data)  #error should include fixed name

    def test_create_tenant_unauthenticated(self):
        # Create new client without force_authenticate
        unauth_client=APIClient()

        payload={
            "name":"Unauthorized Org"
        }

        response= unauth_client.post("/api/tenants/create/",payload,format="json")

        self.assertEqual(response.status_code,401)  #Unauthorized

    def test_duplicate_tenant_name(self):
        # Create first tenant
        Tenant.objects.create(name="Test Org",owner=self.user)

        payload={
            "name":"Test Org"
        }

        response=self.client.post("/api/tenants/create/",payload,format="json")

        self.assertEqual(response.status_code,400)
        self.assertIn('name',response.data)