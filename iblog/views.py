from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from .models import Post, Comment
from .forms import (CommentForm, UserProfileForm, 
					EditProfileForm, CreateUserForm,
					UserLoginForm
	)

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user

@unauthenticated_user
def register(request):
	template_name = 'register.html'
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}!')
			return redirect('login_user')

	context = {'form': form}
	return render(request, template_name, context)


@unauthenticated_user
def login_user(request):
	template_name = 'login.html'

	next = request.GET.get('next') #testing next functionality
	#url_is_safe = is_safe_url(next, allowed_hosts, require_https=False)

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if next:# and url_is_safe:
			login(request, user)
			return redirect(next)

		if user is not None:
			login(request, user)
			return redirect('home')

		else:
			messages.info(request, f'Username OR Password is incorrect')
			return redirect('login_user')
			return render(request, 'login.html')

	context = {}
	return render(request, template_name, context)


'''
@unauthenticated_user
def login_user(request):
	template_name = 'login.html'
	form = UserLoModuleNotFoundError: No module named 'general'
ginForm()

	if request.method == 'POST':
		form = UserLoginForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')

			#username = request.POST.get('username')
			#password = request.POST.get('password')
			print('stage1')
			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				print('stage2')
				return redirect('home')


			else:
				messages.info(request, f'Username OR Password is incorrect') 	
				return render(request, 'login.html')

	context = {'form':form}
	return render(request, template_name, context)
'''


#@login_required(login_url='login_user')
def logout_user(request):
	logout(request)
	return redirect('login_user')


class PostList(generic.ListView):
	template_name = 'index.html'
	queryset = Post.objects.filter(status=1).order_by('-created_on') 
	context_object_name = 'posts' #revisit later
	paginate_by = 2

class PostDetail(generic.DetailView):
	model = Post
	template_name = 'post_detail.html'

class PostCreate(generic.CreateView):
	model = Post
	template_name = 'post_form.html'
	fields = ['title', 'content', 'status']


def user_profile(request):
	template_name = 'user_profile.html'
	
	profile_form = UserProfileForm(instance=request.user.profile)
	context = {'profile_form':profile_form}
	
	return render(request, template_name)


#@unauthenticated_user
@login_required(login_url='login_user')
def edit_profile(request):
	template_name = 'edit_profile.html'
	edit_profile_form = EditProfileForm(instance=request.user.profile)

	next = request.GET.get('next')
	if request.method == 'POST':
		edit_profile_form = EditProfileForm(request.POST, 
									   request.FILES, 
									   instance=request.user.profile
		)

		if edit_profile_form.is_valid(): 
			edit_profile_form.save()
			messages.success(request, f'Success! Your account has been updated!')
			return redirect('user_profile')

	else:
		edit_profile_form = EditProfileForm(instance=request.user.profile)

	context = {'edit_profile_form': edit_profile_form}
	return render(request, template_name, context)



def post_detail(request, slug):
	template_name = 'post_detail.html'
	post = get_object_or_404(Post, slug=slug)
	comments = post.comments.filter(active=True)

	new_comment = None

	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():

			# Create Comment object but don't save to database yet
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.post = post
			# Save the comment to the database
			new_comment.save()


	else:
		comment_form = CommentForm()


	context = {'post':post, 'comments':comments, 'new_comment':new_comment, 'comment_form':comment_form}
	return render(request, template_name, context)	

def error_404_view(request, exception):
	template_name = '404.html'
	return render(request, template_name, status=404)


'''
def error_500_view(request, exception):
	template_name = '500.html'
	return render(request, template_name, status=500)

def custom_500(request):
	template_name = '500.html'
	return render(request, template_name, status=500)
'''
