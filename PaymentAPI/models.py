from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, PermissionsMixin
# Create your models here.



class User(AbstractUser,PermissionsMixin):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email=models.EmailField(unique=True,null=True)
    first_name=models.CharField(max_length=30,null=True,blank=True)
    last_name=models.CharField(max_length=30,null=True,blank=True)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    date_joined=models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    def get_balance(self):
        return self.balance
        
    def __str__(self):
        return str(self.username)

class Transaction(models.Model):
    sender = models.ForeignKey(User,on_delete=models.PROTECT,related_name='sender')
    receiver = models.ForeignKey(User,on_delete=models.PROTECT,related_name='receiver')
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)


    
