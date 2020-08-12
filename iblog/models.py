from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

STATUS = (
	(0, "Draft"),
	(1, "Publish")
)

class Post(models.Model):
	title = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(max_length=200, unique=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
	updated_on = models.DateTimeField(auto_now=True)
	content = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(choices=STATUS, default=0)



	class Meta:
		ordering = ['-created_on']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		kwargs = {'slug': self.slug, 'pk':self.id}

		return reverse("post-pk-slug-detail", kwargs=kwargs)



class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=False)


	class Meta:
		ordering = ['-created_on']

	def __str__(self):
		return 'Comment {self.body} by {self.name}'


class Like(models.Model):
	user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
	liked_on = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return f'{self.id}'


class Profile(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	real_name =  models.CharField(max_length=200, null=True, blank=True)
	profile_pic = models.ImageField(default="default.png", upload_to='images')
	location =  models.CharField(max_length=200, null=True, blank=True)
	occupation =  models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return f'{self.user.username} Profile'