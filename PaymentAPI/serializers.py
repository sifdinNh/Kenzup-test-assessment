from django.db.models import fields
from rest_framework import serializers
from PaymentAPI.models import Transaction,User


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('__all__')
        read_only = ('created_at',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','first_name','last_name','balance')
    