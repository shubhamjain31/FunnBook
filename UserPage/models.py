from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	caption = models.CharField(max_length=200,default='',blank=True)
	image = models.ImageField(upload_to='media')
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.user)+ ' '+ str(self.date.date())

class Profile(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	userImage = models.ImageField(upload_to='media',default='media/profile.jpeg')
	bio = models.CharField(max_length=200,default='',blank=True)
	connection = models.CharField(max_length=100,default='',blank=True)
	follower = models.IntegerField(default=0)
	following = models.IntegerField(default=0)

	def __str__(self):
		return str(self.user)