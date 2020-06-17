from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# upload a user's profile pic to MEDIA_ROOT/user_<id>/<filename>
def profile_pic_path(instance, filename):
	return 'user_{0}/{1}'.format(instance.id, filename)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_pic = models.ImageField(upload_to=profile_pic_path, default="user.png")
	bio = models.TextField(blank=True)
	following = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="followers")

	def __str__(self):
		return f"{self.id} - User: {self.user.username}"

# link Profile model with User model
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


def post_pic_path(instance, filename):
	# upload a user's post pic to MEDIA_ROOT/user_<id>/<filename>
	return 'user_{0}/{1}'.format(instance.user.id, filename)

class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	pic = models.ImageField(upload_to=post_pic_path)
	caption = models.TextField(blank=True)

	def __str__(self):
		return f"{self.id} - User: {self.user.username}, Date: {self.date}"


class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post_id = models.IntegerField()

	def __str__(self):
		return f"{self.id} - User: {self.user.username}, Post ID: {self.post_id}"


class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	post_id = models.IntegerField()
	text = models.TextField()

	def __str__(self):
		return f"{self.id} - User: {self.user.username}, Date: {self.date}, Post ID: {self.post_id}"