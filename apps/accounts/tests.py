from django.test import TestCase
from apps.accounts.models import CustomUser

class AccountsTestCase(TestCase):
    def setUp(self):
        self.staff_user = CustomUser.objects.create_user(
            username='teststaff',
            password='Password123!',
            role=CustomUser.Roles.STAFF
        )
        self.admin_user = CustomUser.objects.create_superuser(
            username='testadmin',
            password='Password123!',
            role=CustomUser.Roles.ADMIN
        )

    def test_user_roles(self):
        """Verify role assignment and superuser properties."""
        self.assertEqual(self.staff_user.role, 'STAFF')
        self.assertEqual(self.admin_user.role, 'ADMIN')
        self.assertTrue(self.admin_user.is_superuser)
        self.assertFalse(self.staff_user.is_superuser)

    def test_token_auto_generation(self):
        """Verify that an API token is automatically generated via signals."""
        self.assertIsNotNone(self.staff_user.auth_token.key)
        self.assertIsNotNone(self.admin_user.auth_token.key)