from django.urls import path
from .views import *

urlpatterns = [
    path('', Cart.as_view(), name='cart'),
    path('<int:pk>/', PreviousCart.as_view(), name='previous_cart'),

    # ajax
    path('delete-item/<int:pk>/', DeleteItemView.as_view(), name='delete-item'),
    path('counter-input/<int:pk>/', CounterInput.as_view(), name='counter-input'),

    path('checkout/<int:order_pk>/', Checkout.as_view(), name='checkout'),
]
