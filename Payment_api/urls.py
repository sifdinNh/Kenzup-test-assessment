from django.contrib import admin
from django.urls import path
from Payment_api import views
urlpatterns = [
    path('ledger',views.TransactionListAPIView.as_view(),name="ledger"),
    path('transfer',views.TransferAPIView.as_view(),name="transfer"),
    path('balance/<uuid:id>',views.BalanceAPIView,name="balance"),
]
