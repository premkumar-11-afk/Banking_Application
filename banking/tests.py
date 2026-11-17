from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Account, Transaction

class BankingFlowTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="TestPass123!")
        self.bob = User.objects.create_user(username="bob", password="TestPass123!")
        self.alice_account = Account.objects.create(user=self.alice, account_number="SB11111111", balance=Decimal("1000.00"))
        self.bob_account = Account.objects.create(user=self.bob, account_number="SB22222222", balance=Decimal("500.00"))

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_login_success(self):
        response = self.client.post(reverse("login"), {"username": "alice", "password": "TestPass123!"})
        self.assertEqual(response.status_code, 302)

    def test_successful_transfer_updates_both_balances(self):
        self.client.login(username="alice", password="TestPass123!")
        response = self.client.post(reverse("transfer"), {
            "recipient_account": "SB22222222", "amount": "100.00", "description": "Test transfer"
        })
        self.assertEqual(response.status_code, 302)
        self.alice_account.refresh_from_db()
        self.bob_account.refresh_from_db()
        self.assertEqual(self.alice_account.balance, Decimal("900.00"))
        self.assertEqual(self.bob_account.balance, Decimal("600.00"))
        self.assertEqual(Transaction.objects.count(), 1)

    def test_insufficient_balance_is_rejected(self):
        self.client.login(username="alice", password="TestPass123!")
        response = self.client.post(reverse("transfer"), {
            "recipient_account": "SB22222222", "amount": "5000.00"
        })
        self.assertEqual(response.status_code, 200)
        self.alice_account.refresh_from_db()
        self.assertEqual(self.alice_account.balance, Decimal("1000.00"))
        self.assertEqual(Transaction.objects.count(), 0)

    def test_unknown_recipient_is_rejected(self):
        self.client.login(username="alice", password="TestPass123!")
        response = self.client.post(reverse("transfer"), {
            "recipient_account": "SB99999999", "amount": "10.00"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_self_transfer_is_rejected(self):
        self.client.login(username="alice", password="TestPass123!")
        response = self.client.post(reverse("transfer"), {
            "recipient_account": "SB11111111", "amount": "10.00"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_zero_amount_is_rejected(self):
        self.client.login(username="alice", password="TestPass123!")
        response = self.client.post(reverse("transfer"), {
            "recipient_account": "SB22222222", "amount": "0.00"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Transaction.objects.count(), 0)
