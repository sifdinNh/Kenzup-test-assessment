from rest_framework.exceptions import ValidationError
from rest_framework import generics,status
from PaymentAPI.models import Transaction,User
from PaymentAPI.serializers import TransactionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import decimal
from django.shortcuts import get_object_or_404
from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import transaction

# Create your views here.



class TransactionListAPIView(generics.ListAPIView):
    """
    get:
        Parameters: start -> str, end -> str
        Return a list of all the existing payement transactions within a date range.

    """
    serializer_class = TransactionSerializer

    start_date_config = openapi.Parameter(
        'start', in_=openapi.IN_QUERY, description='Start date with format yyyy-mm-dd', type=openapi.TYPE_STRING)
    end_date_config = openapi.Parameter(
        'end', in_=openapi.IN_QUERY, description='End date with format yyyy-mm-dd', type=openapi.TYPE_STRING)    

    @swagger_auto_schema(manual_parameters=[start_date_config,end_date_config])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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
    """
    post:
        Parameters:sender -> uuid, receiver -> uuid, ammount-> decimal
        Create a new Transaction instance. and withdraw the ammount of money from the sender

    """

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
        with transaction.atomic():
            sender = User.objects.filter(id=data.get('sender'))
            receiver = User.objects.filter(id=data.get('receiver'))
            amount=decimal.Decimal(data.get('amount'))
            sender.update(balance=F('balance')-amount)
            receiver.update(balance=F('balance')+amount)
        return super().get_success_headers(data)

@api_view(['GET'])
def BalanceAPIView(request,id):
    """
        Parameters: id -> uuid
        Return The balance of the recieved id user
    """
    user = get_object_or_404(User,id=id)
    return Response({"balance":user.get_balance()})