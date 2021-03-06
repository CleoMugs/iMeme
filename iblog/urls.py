from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from iblog.sitemaps import PostSitemap 
from .feeds import LatestPostsFeed

from django.conf.urls import (handler403, handler404, handler500)
from . import views
from .views import VerificationView

sitemaps = {
	"posts": PostSitemap,
}

handler404 = 'iblog.views.error_404_view'

urlpatterns =[

    path('', views.PostList.as_view(), name='home'),
    path('register/', views.register, name='register_user'),
    path('email_confirm/', views.email_confirm, name='confirm_email'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),

    path('post/new/', views.PostCreate.as_view(), name='post_create'),
	path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
	path("feed/rss", LatestPostsFeed(), name="post_feed"),
	
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),

    path('user/', views.user_profile, name='user_profile'),
	path('edit_profile/', views.edit_profile, name='edit_profile'),

    path('reset_password/', 
    	auth_views.PasswordResetView.as_view(
    		template_name='password_reset.html'), 
    	name="reset_password"),

    path('reset_password_sent/', 
    	auth_views.PasswordResetDoneView.as_view(
    		template_name='password_reset_sent.html'), 
    	name="password_reset_done"),

    path('reset/<uidb64>/<token>/', 
    	auth_views.PasswordResetConfirmView.as_view(
    		template_name='password_reset_form.html'), 
    	name="password_reset_confirm"),

    path('reset_password_complete/', 
    	auth_views.PasswordResetCompleteView.as_view(
    		template_name='password_reset_complete.html'), 
    	name="password_reset_complete"),

    path('<slug:slug>/', views.post_detail, name='post_detail'),
    
    #path('blog/<int:pk>-<slug:slug>/', views.post_detail, name='post_detail'),

    #path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
	

]