from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.views import generic
from rest_framework import generics,status
from rest_framework.serializers import Serializer
from Payment_api.models import Transaction,User
from Payment_api.serializers import TransactionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import decimal
from datetime import datetime as dt
from django.shortcuts import get_object_or_404
from django.db.models import F

# Create your views here.



class TransactionListAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start',None)
        end_date = self.request.query_params.get('end',None)
        if start_date and end_date:
            try:
                queryset = Transaction.objects.filter(created_at__range=[start_date,end_date])
            except Exception as e:
                print(e)
                raise ValidationError({"message":"value has an invalid format. It must be in YYYY-MM-DD"})
        else:
            raise ValidationError({"message":"must specify a date range"})
        return queryset


class TransferAPIView(generics.CreateAPIView):
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sender = serializer.validated_data['sender']
        if sender.get_balance() < serializer.validated_data['amount']:
            return Response({"message":"insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def get_success_headers(self, data):
        sender = User.objects.filter(id=data.get('sender'))
        receiver = User.objects.filter(id=data.get('receiver'))
        amount=decimal.Decimal(data.get('amount')) 
        sender.update(balance=F('balance')-amount)
        receiver.update(balance=F('balance')+amount)
        return super().get_success_headers(data)