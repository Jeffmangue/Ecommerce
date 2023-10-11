from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
import datetime


def index(request):
	valuenext = ""
	if request.user.is_authenticated:
		if valuenext != "":
			return redirect(valuenext)
		return redirect('homepage')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')
			valuenext= request.POST.get('next')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				if valuenext != "":
					return redirect(valuenext)
				return redirect('homepage')
			else:
				messages.error(request, 'Wrong username or password')
				return render(request, 'login/index.html')
		return render(request, 'login/index.html')


