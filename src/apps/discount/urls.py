from django.urls import path
from .views import *

urlpatterns = [
    path('create-CashDiscount/', CashDiscountCreateView.as_view(),
         name='create_CashDiscount'),
    path('create-PercentageDiscount/', PercentageDiscountCreateView.as_view(),
         name='create_PercentageDiscount'),
    path('create-CodeDiscount/', CodeDiscountCreateView.as_view(),
         name='create_CodeDiscount'),
]
