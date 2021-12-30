from rest_framework.test import APITestCase
from django.urls import reverse
class TransactionTestCase(APITestCase):
    
    def setUp(self):
        self.transaction_list_url=reverse('ledger')
        return super().setUp()

    def test_get_ledger_witout_date_range(self):
        response=self.client.get(self.transaction_list_url)
        self.assertEqual(response.status_code,400)

    def test_get_ledger_with_invalid_date_format(self):
        response=self.client.get(f"{self.transaction_list_url}?start=2021-3-d&end=2021-02-01")
        self.assertEqual(response.status_code,400)

    def test_get_ledger_with_valid_date_range(self):
        response=self.client.get(f"{self.transaction_list_url}?start=2021-12-03&end=2021-12-30")
        self.assertEqual(response.status_code,200)