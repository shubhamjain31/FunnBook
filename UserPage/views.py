from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Post, Profile, Like, Following
from django.contrib import messages
import json
from django.views.generic import ListView
from django.views import View
from django.core.paginator import Paginator
from django.urls import reverse

# Create your views here.

def userHome(request):
	user = Following.objects.get(user = request.user)
	followed_users = user.followed.all()
	posts = Post.objects.filter(user__in = followed_users).order_by('-pk') | Post.objects.filter(user = request.user).order_by('-pk')
	liked_ = [i for i in posts if Like.objects.filter(post=i, user=request.user)]
	activeUser = Profile.objects.get(user=request.user)
	params = {'posts':posts,"liked_post":liked_,"user":activeUser}
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
	activeUser = Profile.objects.get(user=request.user)
	if user:
		user = user[0]
		profile = Profile.objects.get(user=user)

		#collect all the posts from getpost() function
		post = getPost(user)
		bio = profile.bio
		conn = profile.connection
		user_img = profile.userImage
		is_following = Following.objects.filter(user=request.user,followed=user)

		#create a Following objects
		following_obj = Following.objects.get(user = user)
		follower = following_obj.follower.count()
		following = following_obj.followed.count()
		params = {'user_obj':user,'bio':bio,'conn':conn,'follower':follower,'following':following,'userImg':user_img,'posts':post,'connection':is_following,"user":activeUser}
	else:
		return HttpResponse("No Such User")
	return render(request, "userpage/userProfile.html", params)

#this function divide the user three post in each row and used in userProfile() function
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

class Search_User(ListView):
	model = User
	template_name = "userpage/searchuser.html"
	paginate_by = 2

	#this function is a combination of list of queryset and list of user profile image in template file
	def get_queryset(self):
		search = self.request.GET.get("search","")
		queryset = User.objects.filter(username__icontains=search)
		userProfile = []
		for i in queryset:
			userProfile.append(Profile.objects.filter(user=i.id))
		return list(zip(queryset,userProfile))

	#this function is used for sending user image path for showing the image on navbar
	def get_context_data(self, **kwargs):
		activeUser = Profile.objects.get(user=self.request.user)
		context = super(Search_User,self).get_context_data(**kwargs)
		context['user'] = activeUser
		return context

class EditProfile(View):
    def post(self, request, *args, **kwargs):
        profile_obj = Profile.objects.get(user = request.user)
        bio = request.POST.get("Bio", "")
        img = request.FILES.get("image", "")
        if bio:
        	profile_obj.bio = bio
        if img:
        	profile_obj.userImage = img
        profile_obj.save()

        return HttpResponseRedirect(reverse("userprofile", args=(request.user.username,)))