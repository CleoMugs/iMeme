from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Profile
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CreateUserForm(UserCreationForm):
	username = forms.CharField(min_length=4, max_length=150, widget=forms.TextInput(attrs={'placeholder':'Username...'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email...'}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password...'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password...'}))

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']



class UserLoginForm(forms.ModelForm):
	username = forms.CharField(min_length=4, max_length=150, widget=forms.TextInput(attrs={'placeholder':'Username...'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password...'}))

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


