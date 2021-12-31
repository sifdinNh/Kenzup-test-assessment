from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import  status
from Payment_api.models import Transaction,User
from Payment_api.serializers import TransactionSerializer



class TransactionTestCase(APITestCase):
    
    def setUp(self):
        self.transaction_list_url=reverse('ledger')
        self.start_date="2021-12-01"
        self.end_date = "2022-01-10"
        self.sender=User.objects.create(username="sender",balance=1000.00)
        self.receiver=User.objects.create(username="receiver",balance=500.00)
        self.response=self.client.post(reverse('transfer'),{'sender':self.sender.id,
                                                            'receiver':self.receiver.id,
                                                            'amount':300.00},format="json")
        self.transaction_list=Transaction.objects.filter(created_at__range=[self.start_date,self.end_date])
        return super().setUp()

    def test_get_ledger_witout_date_range(self):
        response=self.client.get(self.transaction_list_url)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_get_ledger_with_invalid_date_format(self):
        response=self.client.get(self.transaction_list_url,{"start":"2021-3-d","end":"2021-02-01"})
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_get_ledger_with_valid_date_range(self):
        response=self.client.get(self.transaction_list_url,{"start":self.start_date,"end":self.end_date},format="json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        serializer=TransactionSerializer(self.transaction_list,many=True)
        self.assertEqual(response.data,serializer.data)