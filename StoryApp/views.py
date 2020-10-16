from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views import View

# Create your views here.

class Home(View):
	def get(self,request,*args,**kwargs):
		return HttpResponse("Checking.....")