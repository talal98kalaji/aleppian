# accounts/urls.py
from django.urls import path,include
from .views import RegisterView, LoginView, CreateSuperUserView,UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/',  LoginView.as_view(),  name='login'),
    path('create-superuser/', CreateSuperUserView.as_view(), name='create-superuser'),
    path('', include(router.urls)),
]
