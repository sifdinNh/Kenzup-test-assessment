from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.views import generic
from rest_framework import generics,status
from rest_framework.serializers import Serializer
from api.models import Transaction,User
from api.serializers import TransactionSerializer
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
            raise ValidationError(detail="must specify a date range")
        return queryset