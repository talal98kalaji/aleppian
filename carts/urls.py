from django.urls import path
from .views import add_cart_item, update_cart_item, remove_cart_item ,get_cart


urlpatterns = [
path('', get_cart),
path('add-item/', add_cart_item),
path('updated-item/', update_cart_item),
path('remove-item/', remove_cart_item)
]