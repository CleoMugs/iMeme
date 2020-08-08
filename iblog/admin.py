from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class PostAdmin(SummernoteModelAdmin):
	list_display = ('title', 'author', 'slug', 'status', 'created_on')
	list_filter = ("status",)
	search_fields = ['title', 'content']
	prepopulated_fields = {'slug':('title',)}
	summernote_fields = ('content',)


class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'body', 'post', 'created_on', 'active')
	list_filter = ('active', 'created_on')
	search_fields = ('name', 'email', 'body')
	actions = ['approve_comments']

	def approve_comments(self, request, queryset):
		queryset.update(active=True)

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'real_name', 'profile_pic', 'location', 'occupation', 'date_created')
	#list_filter = ('active', 'created_on')
	search_fields = ('user',)
	

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile, ProfileAdmin)