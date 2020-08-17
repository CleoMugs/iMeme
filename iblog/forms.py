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


'''
class CreateUserForm(UserCreationForm):
	username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
	email = forms.EmailField(label='Enter email')
	password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

	model = User
	def clean_username(self):
		username = self.cleaned_data['username'].lower()
		r = User.objects.filter(username=username)
		if r.count():
		    raise  ValidationError("Username already exists")
		return username

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		r = User.objects.filter(email=email)
		if r.count():
		    raise  ValidationError("Email already exists")
		return email

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password2 and password1 != password2:
		    raise ValidationError("Password don't match")

		return password2

'''
