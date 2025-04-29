from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import Voucher


# Create your tests here.

class VoucherTest(TestCase):
    def setUp(self):
        now = timezone.now()

        self.valid_voucher = Voucher.objects.create(
            code='1234',
            valid_from=now - timedelta(days=10),
            valid_to=now + timedelta(days=10),
            discount=20,
            active=True
        )

        self.expired_voucher = Voucher.objects.create(
            code='4321',
            valid_from=now - timedelta(days=10),
            valid_to=now - timedelta(days=10),
            discount=20,
            active=True
        )

    def test_valid_voucher(self):
        now = timezone.now()
        self.assertTrue(self.valid_voucher.active)
        self.assertTrue(self.valid_voucher.valid_from <= now <= self.valid_voucher.valid_to)

    def test_expired_voucher(self):
        now = timezone.now()
        self.assertTrue(self.expired_voucher.active)
        self.assertFalse(self.expired_voucher.valid_to >= now)

