from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from UserPage.models import Profile

#used whenever new user registered then his/her profile will created using signals
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)