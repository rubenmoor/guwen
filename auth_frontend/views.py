from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from forms import *

def login(request):
	if request.method == 'POST':
		form = LoginForm(data=request.POST)
		if form.is_valid():
			auth_login(request, form.get_user())
			if not form.cleaned_data['remember']:
				request.session.set_expiry(0)
			messages.success(request, 'Login successful.')
			return redirect(request.POST['next'])
	else:
		form = LoginForm()
	return render(request, 'login.html', {
		'form': form,
		'next': request.GET.get('next') or '/',
		})	

def logout(request):
	auth_logout(request)
	messages.success(request, 'Successfully logged out. Bye!')
	return redirect('home')

def user_new(request):
	if request.method == 'POST':
		form = UserNewForm(data=request.POST)
		if form.is_valid():
			username = form.clean_username()
			password = form.clean_password2()
			form.save()
			user = authenticate(username=username, password=password)
			auth_login(request, user)
			messages.success(request, 'Registration successful.')
			return redirect('home')
	else:
		form = UserNewForm()
	return render(request, 'user_new.html', {
		'form': form,
		})

@login_required
def user_change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(user=request.user, data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Password change successful.')
			return redirect('home')
	else:
		form = PasswordChangeForm(user=request.user)
	return render(request, 'user_change_password.html', {
		'form': form,
		})	

@login_required
def user_change_email(request):
	if request.method == 'POST':
		form = UserChangeEmailForm(instance=request.user, data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Email change successful.')
			return redirect('home')
	else:
		form = UserChangeEmailForm(instance=request.user)
	return render(request, 'user_change_email.html', {
		'form': form,
		})	