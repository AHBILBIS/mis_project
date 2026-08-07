from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import CustomUser
from apps.departments.models import Department

class StaffAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='apiuser',
            password='Password123!',
            role=CustomUser.Roles.MANAGER
        )
        self.dept = Department.objects.create(name='IT Support', code='IT')

    def test_unauthenticated_api_access_denied(self):
        """Verify that unauthenticated API requests are blocked (401 Unauthorized)."""
        response = self.client.get(reverse('api_staff_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_api_access_allowed(self):
        """Verify that token-authenticated users can access staff API endpoints."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        response = self.client.get(reverse('api_staff_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)