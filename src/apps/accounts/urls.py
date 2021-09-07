from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    # آدرس های مربوط به مشتری
    path('orders/', OrderHistory.as_view(), name='orders'),
    path('<int:pk>/edit/', CustomerEditProfile.as_view(), name='edit'),
    path('create-address/', CreateAddress.as_view(), name='create_address'),
    path('edit-address/<int:pk>/', EditAddress.as_view(), name='edit_address'),
    path('delete-address/<int:pk>/', DeleteAddress.as_view(), name='delete_address'),

    # آدرس مربوط به گزارش گیری مدیر
    path('report/', Report.as_view(), name='report'),
]
