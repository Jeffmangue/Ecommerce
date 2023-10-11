from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('validate_username', views.validate_username, name='validate_username'),
    path('validate_email', views.validate_email, name='validate_email'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
 