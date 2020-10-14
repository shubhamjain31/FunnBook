from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def home(request):
	return render(request, "signup.html")

def signup(request):
	if request.method == "POST":
		email = request.POST.get('email','')
		fname = request.POST.get('fname','')
		lname = request.POST.get('lname','')
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		Cpassword = request.POST.get('cpassword','')

		if password == Cpassword:
			user_save = User.objects.create_user(first_name=fname,last_name=lname,password=password,email=email,username=username)
			user_save.save()

	return render(request, "signup.html")

def user_login(request):
	if request.method == "POST":
		uname = request.POST.get('username','')
		pwrd = request.POST.get('password','')
		user = authenticate(username=uname,password=pwrd)
		if user is not None:
			login(request,user)
			messages.success(request, "Logged In")
			return HttpResponseRedirect('/account/signup/')
		else:
			messages.error(request, "Invalid Username and Password")
			return HttpResponseRedirect('/account/signup/')

def user_logout(request):
	logout(request)
	messages.success(request, "Logged Out")
	return HttpResponseRedirect('/account/signup/')