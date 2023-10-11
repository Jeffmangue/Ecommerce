from django.urls import path
from . import views

urlpatterns = [
	path('', views.notifications, name='notifications'),
	path('add-user-to-the-group', views.add_user_to_the_group, name='add_user_to_the_group'),
]
