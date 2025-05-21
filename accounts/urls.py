# accounts/urls.py
from django.urls import path,include
from .views import current_user, RegisterView, LoginView, CreateSuperUserView,CreateDataEntryView, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/',  LoginView.as_view(),  name='login'),
    path('create-superuser/', CreateSuperUserView.as_view(), name='create-superuser'),
    path('create-data-entry/', CreateDataEntryView.as_view(), name='create-data-entry'),
    path('', include(router.urls)),
    path('user/', current_user, name='current-user'),
]
