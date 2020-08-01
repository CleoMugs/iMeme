from django.shortcuts import render
from django.views import generic
from .models import Post


class PostList(generic.ListView):
	#model = Post
	queryset = Post.objects.filter(status=1).order_by('-created_on')
	template_name = 'index.html'
	#ordering = ['-created_on']


class PostDetail(generic.DetailView):
	model = Post
	template_name = 'post_detail.html'