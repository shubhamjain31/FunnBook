from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Post, Profile
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

def postDelete(request, postId):
	post_ = Post.objects.filter(pk=postId)
	image_path = post_[0].image.url
	post_.delete()
	messages.info(request, "Post Deleted !!")
	return HttpResponseRedirect('/userpage')

def userProfile(request, username):
	user  = User.objects.filter(username=username)
	if user:
		user = user[0]
		profile = Profile.objects.get(user=user)
		post = getPost(user)
		bio = profile.bio
		conn = profile.connection
		follower = profile.follower
		following = profile.following
		user_img = profile.userImage
		params = {'user_obj':user,'bio':bio,'conn':conn,'follower':follower,'following':following,'userImg':user_img,'posts':post}
	else:
		return HttpResponse("No Such User")
	return render(request, "userpage/userProfile.html", params)

def getPost(user):
	allpost = Post.objects.filter(user=user)
	print(allpost)
	image_list = [allpost[i:i+3] for i in range(0,len(allpost),3)]
	print(image_list)
	return image_list