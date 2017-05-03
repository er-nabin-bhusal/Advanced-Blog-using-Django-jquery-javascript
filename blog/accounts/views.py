from django.shortcuts import render,redirect
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)

from .forms import UserLoginForm,UserRegistrationForm
# Create your views here.

def login_view(request):

	next = request.GET.get('next')

	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username,password=password)
		login(request,user)
		if next:
			return redirect(next)
		return redirect("/")
	context ={
	"form":form,
	"title":title,
	}
	return render(request,"form.html",context)


def register_view(request):
	next = request.GET.get('next')

	title = "Register"
	form = UserRegistrationForm(request.POST or None)
	if form.is_valid() and not request.user.is_authenticated():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username,password=password)
		login(request, new_user)
		if next:
			return redirect(next)
		return redirect("/")

	context = {
	'title':title,
	'form':form,
	}
	return render(request,"form.html",context)


def logout_view(request):
	logout(request)
	return redirect("/")






