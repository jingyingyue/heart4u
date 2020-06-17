import base64
import uuid

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render
from django.urls import reverse

from .models import  Post, Like, Comment
from .forms import ProfileForm

# Create your views here.
@login_required
def index(request):
	""" show posts from user's following """
	# get user's following
	following = []
	for user in request.user.profile.following.all():
		following.append(user.user)

	# create context to pass info
	context = {
		"posts": Post.objects.filter(user__in=following).order_by('-date')
	}

	# redirect user to home page
	return render(request, "heart4u/index.html", context)


def register_view(request):
	""" register a new user """
	if request.method=="POST":
		# get inputs from form
		first_name = request.POST["first_name"]
		last_name = request.POST["last_name"]
		email = request.POST["email"].lower()
		username = request.POST["username"].lower()
		password = request.POST["password"]
		confirm_password = request.POST["confirm_password"]

		# check if email already registered
		if User.objects.filter(email=email).exists():
			messages.error(request, "Email already registered")
			return HttpResponseRedirect(reverse("register"))
		
		# check if username already exists
		elif User.objects.filter(username=username).exists():
			messages.error(request, "Username already exists")
			return HttpResponseRedirect(reverse("register"))

		# check if two passwords do not match
		elif password!=confirm_password:
			messages.error(request, "Passwords do not match")
			return HttpResponseRedirect(reverse("register"))

		else:
			# create new user object and add to database
			user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
			user.save()

			# redirect user to login page
			messages.success(request, "Account created")
			return HttpResponseRedirect(reverse("login"))

	else:
		return render(request, "heart4u/register.html")


def login_view(request):
	""" login a user """
	if request.method=="POST":
		# check if user entered valid username and password
		username = request.POST["username"].lower()
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)

		# if valid, login user and redirect to home page
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))

		# if invalid, redirect user back to login page
		else:
			messages.error(request, "Invalid username/password")
			return HttpResponseRedirect(reverse("login"))

	else:
		return render(request, "heart4u/login.html")


@login_required
def logout_view(request):
	""" logout a user """
	# redirect user to login page
	logout(request)
	messages.success(request, "Logged out")
	return HttpResponseRedirect(reverse("login"))


@login_required
def profile_view(request, username=None):
	""" show a user's profile """
	# check if profile user = request user
	if not username:
		profile_user = request.user
	else:
		profile_user = User.objects.get(username=username)

	# create context to pass info
	context = {
		"user": profile_user,
		"following": profile_user.profile.following.all(),
		"followers": profile_user.profile.followers.all(),
		"posts": Post.objects.filter(user=profile_user).order_by('-date'),
		"profile_pic_form": ProfileForm(instance=profile_user.profile)
	}

	# redirect user to profile page
	return render(request, "heart4u/profile.html", context)


@login_required
def edit_profile(request):
	""" edit and update a user's profile """
	if request.method=="POST":
		# get inputs from form
		user = User.objects.get(id=request.user.id)
		new_username = request.POST["username"].lower()
		new_firstname = request.POST["first_name"]
		new_lastname = request.POST["last_name"]
		new_bio = request.POST["bio"]
		new_profilepic = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

		# check if user updated profile pic
		if new_profilepic.is_valid():
			new_profilepic.save()

		# check if user updated username
		if new_username!=user.username:
			# check if new username already exists
			if User.objects.filter(username=new_username).exists():
				messages.error(request, "Username taken, please try again")
				return HttpResponseRedirect(reverse("profile"))
			else:
				user.username = new_username

		# check if user updated first name
		if new_firstname!=user.first_name:
			user.first_name = new_firstname

		# check if user updated last name
		if new_lastname!=user.last_name:
			user.last_name = new_lastname

		# check if user updated bio
		if new_bio!=user.profile.bio:
			user.profile.bio = new_bio
		
		# save updates to database
		user.save()

		# add success message
		messages.success(request, "Profile updated")

		# redirect user to profile page
		return HttpResponseRedirect(reverse("profile"))

	else:
		return HttpResponseNotAllowed(["POST"])


@login_required
def follow_user(request):
	""" follow a user """
	if request.method=="POST":
		# get input from form
		user_id = request.POST["user_id"]

		# add user to request.user's following and save to database
		user = User.objects.get(id=user_id)
		req_user = User.objects.get(id=request.user.id)
		req_user.profile.following.add(user.profile)
		req_user.save()

		# redirect request.user back to user's profile page
		return HttpResponseRedirect(reverse("profile", args=(user.username,)))
	
	else:
		return HttpResponseNotAllowed(["POST"])


@login_required
def unfollow_user(request):
	""" unfollow a user """
	if request.method=="POST":
		# get input from form
		user_id = request.POST["user_id"]

		# remove user from request.user's following and save to database
		user = User.objects.get(id=user_id)
		req_user = User.objects.get(id=request.user.id)
		req_user.profile.following.remove(user.profile)
		req_user.save()

		# redirect request.user back to user's profile page
		return HttpResponseRedirect(reverse("profile", args=(user.username,)))

	else:
		return HttpResponseNotAllowed(["POST"])


@login_required
def search(request):
	""" search for users/posts """
	if request.method=="POST":
		# get input from form
		search = request.POST["search"]

		# create context to pass info
		context = {
			"users": User.objects.filter(username__icontains=search).order_by('username'),
			"posts": Post.objects.filter(caption__icontains=search).order_by('-date')
		}

		# redirect user to search page
		return render(request, "heart4u/search.html", context)

	else:
		return HttpResponseNotAllowed(["POST"])


@login_required
def upload_view(request):
	""" upload a post """
	if request.method=="POST":
		# get inputs from form
		pic = request.POST["pic"]
		caption = request.POST["caption"]

		# create post
		post = Post.objects.create(user=request.user, caption=caption)

		# save pic to post
		format, imgstr = pic.split(';base64,')
		ext = format.split('/')[-1]
		data = ContentFile(base64.b64decode(imgstr))
		file_name = f"{str(uuid.uuid4())}.{ext}"
		post.pic.save(file_name, data, save=True)

		# redirect user to profile page
		return HttpResponseRedirect(reverse("profile"))

	else:
		return render(request, "heart4u/upload.html")


@login_required
def post_view(request, username, post_id):
	""" view a post """
	# check if request.user liked the post
	likes = Like.objects.filter(post_id=post_id)
	already_liked = False
	for like in likes:
		if like.user==request.user:
			already_liked = True

	# create context to pass info
	context = {
		"post": Post.objects.get(id=post_id),
		"likes": likes,
		"comments": Comment.objects.filter(post_id=post_id).order_by('-date'),
		"already_liked": already_liked
	}

	# redirect user to post page
	return render(request, "heart4u/post.html", context)


@login_required
def like_unlike(request):
	""" like/unlike a post """
	if request.method=="POST":
		# get input from form
		post_id = request.POST["post_id"]
		state = request.POST["state"]

		# check if user is unliking a post
		if state=='unlike':
			# remove like object associated with user and post
			Like.objects.get(user=request.user, post_id=post_id).delete()

		else:
			# create like object and add to database
			new_like = Like.objects.create(user=request.user, post_id=post_id)
			new_like.save()

		# redirect user to post page
		post_user = Post.objects.get(id=post_id).user
		return HttpResponseRedirect(reverse("post", args=(post_user.username, post_id)))

	else:
		return HttpResponseNotAllowed(["POST"])


@login_required
def comment(request):
	""" comment on a post """
	if request.method=="POST":
		# get input from form
		post_id = request.POST["post_id"]
		comment = request.POST["comment"]

		# create comment object and add to database
		comment = Comment.objects.create(user=request.user, post_id=post_id, text=comment)
		comment.save()

		# redirect user to post page
		post_user = Post.objects.get(id=post_id).user
		return HttpResponseRedirect(reverse("post", args=(post_user.username, post_id)))

	else:
		return HttpResponseNotAllowed(["POST"])