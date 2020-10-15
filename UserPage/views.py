from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Post, Profile, Like, Following
from django.contrib import messages
import json

# Create your views here.

def userHome(request):
	posts = Post.objects.all().order_by('-pk')
	liked_ = [i for i in posts if Like.objects.filter(post=i, user=request.user)]
	params = {'posts':posts,"liked_post":liked_}
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
	image_list = [allpost[i:i+3] for i in range(0,len(allpost),3)]
	return image_list

def likePost(request):
	post_Id = request.GET.get('likeId','')
	post = Post.objects.get(pk=post_Id)
	user = request.user
	like = Like.objects.filter(post=post,user=user)
	liked = False
	if like:
		Like.dislike(post, user)
	else:
		liked = True
		Like.like(post, user)
	resp = {
		"liked":liked
	}
	response = json.dumps(resp)
	return HttpResponse(response, content_type="application/json")

def comment(request):
	comment_ = request.GET.get('comment', '')
	return render(request, "userpage/comments.html")

def follow(request, username):
	login_user = request.user
	to_follow = User.objects.get(username=username)

	#check if already following or not
	following = Following.objects.filter(user = login_user, followed = to_follow)
	is_following = True if following else False

	if is_following:
		#if already follow then unfollow the user
	    Following.unfollow(login_user, to_follow)
	    is_following = False
	else:
		#if not already follow then follow the user
	    Following.follow(login_user, to_follow)
	    is_following = True

	resp = {
	    "following" : is_following,
	}

	response = json.dumps(resp)
	return HttpResponse(response, content_type="application/json")
