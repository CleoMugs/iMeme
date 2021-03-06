from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from .models import Post, Comment
from .forms import (CommentForm, UserProfileForm, 
					EditProfileForm, CreateUserForm,
					UserLoginForm
	)
from django.contrib.auth.models import User
from django.views import View
from django.urls import reverse

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect

from .decorators import unauthenticated_user

from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import token_generator


@unauthenticated_user
def register(request):
	template_name = 'register.html'
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)

		# Get details
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password1'] 

		if form.is_valid():

			if not User.objects.filter(email=email).exists():
				print('Email is unique')

				#title='signup'
				#context = {'form': form, 'title':title}
				#return render(request, template_name, context)

				# checking if user is active
				user =  User.objects.create_user(username=username, email=email, password=password)
				user.is_active = False
				user.save()
				#form.save()


				uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

				#domain = get_current_site(request).domain
				domain = '127.0.0.1:8000'
				
				link = reverse('activate', kwargs={
							   'uidb64':uidb64, 
							   'token':token_generator.make_token(user)})

				activate_url = 'http://' + domain+link #.lstrip('/')

				email_subject = 'Activate Your Account'
				email_body = 'Hi'+ ' ' + user.username + ' ' +'Please click on the link below to activate your account \n\n\n' + activate_url
				
				email = EmailMessage(
				    email_subject,
				    email_body,
				    'noreply@imeme.com',
				    [email],
				)
				email.send(fail_silently=True)

			
				username = form.cleaned_data.get('username')
				messages.success(request, f'Account created successfully for {username}!')
				return redirect('confirm_email')

			else:
				messages.warning(request, f'Email is already taken. Please choose a different email.')
				return redirect('register_user')

	title='signup'
	context = {'form': form, 'title':title}
	return render(request, template_name, context)



class VerificationView(View):
	def get(self, request, uidb64, token):
		'''
		try:	
			id = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=id)

			if not account_activation_token.check_token(user, token):
				print('Already activated')
				return redirect('login_user'+'?message='+'User already activated')


			if user.is_active:
				print('active')
				return redirect('login_user')

			user.is_active = True
			user.save()

			messages.success(request, 'Account activated successfully!')
			return redirect('login_user')

		except Exception as ex:
			pass
		'''

		id = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=id)


		user.is_active = True
		user.save()

		messages.success(request, 'Account activated successfully!')
		return redirect('login_user')
		

class LoginView(View):
	template_name = 'login.html'
	def get(self, request):
		return render(request, 'login.html')


def email_confirm(request):
    template_name = 'email_confirm.html'
    return render(request, template_name)


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
			#return render(request, 'login.html')

	title = 'login'
	context = {'title':title}
	return render(request, template_name, context)


#@login_required(login_url='login_user')
def logout_user(request):
	logout(request)
	return redirect('login_user')


class PostList(generic.ListView):
	template_name = 'index.html'
	#queryset = Post.objects.filter(status=1).order_by('-created_on') 
	queryset = Post.objects.order_by('-created_on') 
	context_object_name = 'posts' #revisit later
	paginate_by = 2

class PostDetail(generic.DetailView):
	model = Post
	template_name = 'post_detail.html'
	query_pk_and_slug = True

class PostCreate(LoginRequiredMixin, generic.CreateView):
	model = Post
	template_name = 'post_form.html'
	fields = ['title', 'content'] #, 'slug', 'status']
	success_url = '/'
	login_url = '/login/'
	redirect_field_name = '/post/new/'
	#success_message = ''

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	'''
	def get_success_url(self):
		return force_text(self.request.GET.get('next', self.success_url))
	'''


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



def post_detail(request,slug):
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
			return HttpResponseRedirect(request.path_info)

	else:
		comment_form = CommentForm()

	context = {'post':post, 'comments':comments, 'new_comment':new_comment, 'comment_form':comment_form}
	return render(request, template_name, context)	


def like(request, post_id):
	new_like, liked_on = Like.objects.get_or_create(user=request.user, post_id=post_id)

	if not liked_on:
		p = Post.objects.get(...)
		number_of_likes = p.like_set.all().count()
	else:
		pass


def error_404_view(request, exception):
	template_name = '404.html'
	return render(request, template_name, status=404)


'''
def error_500_view(request, exception):
	template_name = '500.html'
	return render(request, template_name, status=500)

'''

'''
@unauthenticated_user
def register(request):
	template_name = 'register.html'
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)

		# Get details
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password1'] 


		if form.is_valid():
			if not User.objects.filter(email=email).exists:
				print('Email is unique')
				form.save()
				username = form.cleaned_data.get('username')
				messages.success(request, f'Account created for {username}!')
				return redirect('login_user')
			else:
				messages.warning(request, f'Email is already taken. Please choose a different email.')
				return redirect('register_user')

	context = {'form': form}
	return render(request, template_name, context)
'''