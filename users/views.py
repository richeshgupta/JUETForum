from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.core.mail import send_mail
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .forms import kk
def not_logged_in(request):
	return render(request,'users/not_logged_in.html',{})

def menu(request):
	return render(request,'users/initial.html',{})
	
def about(request):
	return render(request,'users/about.html',{})


def signup_view(request):
	if request.method == 'POST':
		form = kk(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			form.save()
			messages.success(request, f'Account Created for {username}!')
			return redirect('login')
	else:
		form = kk()
	return render(request,'users/signup.html',{'form':form})

