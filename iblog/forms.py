from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Profile
from django import forms
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ['username', 'password']


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name', 'email', 'body')


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['real_name', 'profile_pic', 'location', 'occupation']


class EditProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['real_name', 'location', 'occupation', 'profile_pic']
