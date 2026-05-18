from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Transaction


class UserSpecificTransactionTests(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(
            username='alice',
            password='SecurePass123!',
        )
        self.user_b = User.objects.create_user(
            username='bob',
            password='SecurePass123!',
        )
        self.tx_a = Transaction.objects.create(
            user=self.user_a,
            title='Alice Lunch',
            amount=Decimal('100.00'),
            transaction_type='Expense',
            category='Food',
            date='2026-05-18',
        )
        self.tx_b = Transaction.objects.create(
            user=self.user_b,
            title='Bob Salary',
            amount=Decimal('5000.00'),
            transaction_type='Income',
            category='Salary',
            date='2026-05-18',
        )

    def test_home_shows_only_own_transactions(self):
        client = Client()
        client.login(username='alice', password='SecurePass123!')
        response = client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice Lunch')
        self.assertNotContains(response, 'Bob Salary')

    def test_cannot_delete_other_users_transaction(self):
        client = Client()
        client.login(username='alice', password='SecurePass123!')
        response = client.get(
            reverse('delete_transaction', args=[self.tx_b.id]),
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Transaction.objects.filter(id=self.tx_b.id).exists())

    def test_new_transaction_is_linked_to_logged_in_user(self):
        client = Client()
        client.login(username='bob', password='SecurePass123!')
        client.post(
            reverse('home'),
            {
                'title': 'Bob Coffee',
                'amount': '25.00',
                'transaction_type': 'Expense',
                'category': 'Food',
                'date': '2026-05-19',
            },
        )

        new_tx = Transaction.objects.get(title='Bob Coffee')
        self.assertEqual(new_tx.user, self.user_b)
