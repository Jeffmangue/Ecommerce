from operator import imod
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import urllib.request as urllib
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
import json
import urllib
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib import messages 
from .forms import SignUpForm
from django.forms import ValidationError
from django.contrib.auth.models import Group
from django.core.mail import send_mail
import requests
from notifications.models import NotificationsModel

UserModel = get_user_model()

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            messages.success(request, "Registration successfully, please check your email for confirmation!")
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('register/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            from_email = settings.EMAIL_HOST_USER
            email = EmailMessage(
                mail_subject, message, from_email,to=[to_email]
            )
            email.send()
            return redirect('register')
           
        else:
            messages.error(request, form.errors)
    else:
        form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'register/register.html', context)


def activate(request, uidb64, token):
    form = ""
    context = {
        'form': form
    }
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        superusers = User.objects.filter(is_superuser=True)
        done = []
        for us in superusers:
            if us in done:
                pass
            else:
                group = Group.objects.get(name='lbbc-cainta')
                nt = NotificationsModel(sender=user,receiver=us,subject='Has registered',group=group)
                nt.save()
                done.append(us)
        return render(request, 'register/activation_complete.html', context)
    else:
        return render(request, 'register/activation_invalid.html', context)


def validate_username(request):
    """Check username availability"""
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)

def validate_email(request):
    """Check email availability"""
    email = request.GET.get('email', None)
    response = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(response)


# with captcha
# def register(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST or None)
#         if form.is_valid():
#             recaptcha_response = request.POST.get('g-recaptcha-response')
#             data = {
#                 'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
#                 'response': recaptcha_response
#             }
#             r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
#             result = r.json()
#             if result['success']:
#                 messages.success(request, "Registration successfully, please check your email for confirmation!")
#                 user = form.save(commit=False)
#                 user.is_active = False
#                 user.save()

#                 current_site = get_current_site(request)
#                 mail_subject = 'Activate your account'
#                 message = render_to_string('register/acc_active_email.html', {
#                     'user': user,
#                     'domain': current_site.domain,
#                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                     'token': default_token_generator.make_token(user),
#                 })
#                 to_email = form.cleaned_data.get('email')
#                 from_email = settings.EMAIL_HOST_USER
#                 email = EmailMessage(
#                     mail_subject, message, from_email,to=[to_email]
#                 )
#                 email.send()
#                 return redirect('register')
#             else:
#                 messages.error(request, "Invalid reCAPTCHA. Please try again.")
#         else:
#             messages.error(request, form.errors)
#     else:
#         form = SignUpForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'register/register.html', context)
