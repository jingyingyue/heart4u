from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['profile_pic']
		labels = {'profile_pic': 'Profile Photo'}