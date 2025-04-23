from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_category),
    path('get/all/', views.get_all_categories),
    path('get/<int:id>/', views.get_category_by_id),
    path('edit/<int:id>/', views.edit_category),
    path('delete/<int:id>/', views.delete_category),
]
