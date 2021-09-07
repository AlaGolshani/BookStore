from django.urls import re_path, path
from .views import *

urlpatterns = [
    path('create-category/', CategoryCreateView.as_view(), name='create_category'),

    path('create-book/', BookCreateView.as_view(), name='create_book'),
    re_path(r'edit-book/<slug:(?P<slug>[-\w]+)>', BookUpdateView.as_view(), name='edit_book'),
    re_path(r'delete-book/<slug:(?P<slug>[-\w]+)>', BookDeleteView.as_view(), name='delete_book'),
    re_path(r'(?P<slug>[-\w]+)/', BookDetailView.as_view(), name='book-detail'),
    # re_path(r'(?P<slug>[-\w]+)/', AddToCart.as_view(), name='add_to_cart'),
]
