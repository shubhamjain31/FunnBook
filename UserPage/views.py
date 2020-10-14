from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Post
from django.contrib import messages

# Create your views here.

def username(request):
	posts = Post.objects.all().order_by('-pk')

	params = {'posts':posts}
	return render(request, "userpage/postfeed.html", params)

def post(request):
	if request.method == "POST":
		image = request.FILES.get('image','')
		caption = request.POST.get('caption','')
		user = request.user
		new_post = Post(image=image,caption=caption,user=user)
		new_post.save()
		messages.success(request, "Post Saved!!")
		return HttpResponseRedirect('/userpage')
	else:
		messages.success(request, "Something Went Wrong")
		return HttpResponseRedirect('/userpage')
	return render(request, "userpage/postfeed.html")