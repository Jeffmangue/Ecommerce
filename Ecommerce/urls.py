from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='login/reset_password.html'), name="reset_password"),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='login/sent_reset_link.html'), name="password_reset_done"),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="login/reset_complete.html"), name="password_reset_complete"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='login/reset_confirm.html'), name="password_reset_confirm"),
    path('admin/', admin.site.urls),
    path('',include('Homepage.urls'))
    path('', include('login.urls')),
    path('register', include('register.urls')),
    path('notifications', include('notifications.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)