from django.test import TestCase
from apps.accounts.models import Customer, Admin


class CustomUserTests(TestCase):
    def test_create_user(self):
        customer = Customer.objects.create_user(
            username='ala.golshani',
            email='ala.golshani@email.com',
            password='1234567@'
        )
        self.assertEqual(customer.username, 'ala.golshani')
        self.assertEqual(customer.email, 'ala.golshani@email.com')
        self.assertTrue(customer.is_active)
        self.assertFalse(customer.is_staff)
        self.assertFalse(customer.is_superuser)

    def test_create_superuser(self):
        admin_user = Admin.objects.create_superuser(
            username='superadmin',
            email='superadmin@email.com',
            password='testpass123'
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
