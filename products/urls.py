from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_product),
    path('get/all/', views.getAll),
    path('get/<int:id>/', views.get_product_by_id),
    path('edit/<int:id>/', views.edit_product),
    path('delete/<int:id>/', views.delete_product),
]

#/api/products/get/all/?title=vas&category=2
#/api/products/get/all/?min_price=10000&max_price=20000
#/api/products/get/all/?ordering=-price
#/api/products/get/all/?page=2&per_page=5