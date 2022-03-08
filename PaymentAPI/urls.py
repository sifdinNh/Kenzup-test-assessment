from django.contrib import admin
from django.urls import path, include
from PaymentAPI import views

urlpatterns = [
    path('ledger',views.TransactionListAPIView.as_view(),name="ledger"),
    path('transfer',views.TransferAPIView.as_view(),name="transfer"),
    path('balance/<uuid:id>',views.BalanceAPIView,name="balance"),
    path('balance/<uuid:id>',views.BalanceAPIView,name="balance"),
    path('auth/',include('rest_framework.urls')),
]
