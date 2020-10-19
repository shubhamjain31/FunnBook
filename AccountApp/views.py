from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from UserPage.models import Profile

from django.views.generic import TemplateView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.

#---------------------------------------------Function Based View---------------------------------------------------------

def home(request):
	if request.user.is_anonymous:
		params = {}
	else:
		activeUser = Profile.objects.get(user=request.user)
		params = {"user":activeUser}
	#return render(request, "index.html")
	return render(request, "account/signup.html",params)

def signup(request):
	if request.method == "POST":
		email = request.POST.get('email','')
		fname = request.POST.get('fname','').capitalize()
		lname = request.POST.get('lname','').capitalize()
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		Cpassword = request.POST.get('cpassword','')

		userCheck = User.objects.filter(username=username) | User.objects.filter(email=mail)

		if userCheck:
			messages.warning(request, "Account Already Present with Given User Name or Email")
			return render(request,'account/signup.html')
		elif password == Cpassword:
			user_save = User.objects.create_user(first_name=fname,last_name=lname,password=password,email=email,username=username)
			user_save.save()

	return render(request, "account/signup.html")

def user_login(request):
	if request.method == "POST":
		uname = request.POST.get('username','')
		pwrd = request.POST.get('password','')
		user = authenticate(username=uname,password=pwrd)
		if user is not None:
			login(request,user)
			messages.success(request, "Logged In")
			return HttpResponseRedirect('/userpage')
		else:
			messages.error(request, "Invalid Username and Password")
			return HttpResponseRedirect('/account/signup/')
	return HttpResponse("Error")

def user_logout(request):
	logout(request)
	messages.success(request, "Logged Out")
	return HttpResponseRedirect('/account/signup/')

#---------------------------------------------Class Based View---------------------------------------------------------

class Change_Password(TemplateView):
    template_name = "account/password_change.html"

    def post(self, request):
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user=request.user)
            messages.success(request, "Password Changed Successfully")
            return HttpResponseRedirect("/")
        else:
            for err in form.errors.values():
                messages.error(request, err)
            return HttpResponseRedirect("/change_password")

    def get(self, request):
        form = PasswordChangeForm(user = request.user)
        activeUser = Profile.objects.get(user=request.user)
        return render(request, self.template_name, {"form":form,"user":activeUser})