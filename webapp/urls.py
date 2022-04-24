from django.urls import path
from . import views

urlpatterns = [
    path('registerUser', views.register_user),
    path('loginUser', views.login_user)
]
