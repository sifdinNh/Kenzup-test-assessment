from django.contrib import admin
from django.urls import path
from Payment_api import views
urlpatterns = [
    path('ledger',views.TransactionListAPIView.as_view(),name="ledger"),
]
