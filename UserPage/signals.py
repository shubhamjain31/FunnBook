from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from UserPage.models import Profile, Following

#used whenever new user registered then his/her profile will created using signals
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		Following.objects.create(user = instance)

@receiver(m2m_changed, sender = Following.followed.through)
def add_follower(sender, instance, action, reverse, pk_set, **kwargs):
	"""
	sender => model which will send signal (Following)
	    instance => username of user who is logged in (request.user)
	    action => pre_add if user followed someone, else pre_remove if user unfollowed by someone
	    reverse => to be honest, I dont Know
	    pk_set => set of primary key of users whom i am following
	"""

	followed_users = [] # list of users main (logged ) user have followed
	logged_user = User.objects.get(username = instance) # user who followed other users
	for i in pk_set:
	    user = User.objects.get(pk = i)
	    following_obj = Following.objects.get(user = user)
	    followed_users.append(following_obj)

	if action == "pre_add":
	    for i in followed_users:
	        i.follower.add(logged_user)
	        i.save()

	if action == "pre_remove":
	    for i in followed_users:
	        i.follower.remove(logged_user)
	        i.save()