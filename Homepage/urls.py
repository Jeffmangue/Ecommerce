from django.urls import path
from . import views


urlpatterns = [
   	path('', views.Homepage, name='Homepage'),
    path('create', views.create, name='create'),
    path('read', views.read, name='read'),
    path('delete', views.delete, name='delete'),
    path('login', views.login, name='login'),
    path('checkout', views.checkout, name='checkout'),
]