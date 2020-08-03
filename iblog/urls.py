from . import views
from django.urls import path
from django.contrib.sitemaps.views import sitemap
from iblog.sitemaps import PostSitemapds 
from .feeds import LatestPostsFeed

sitemaps = {
	"posts": PostSitemap,
}

urlpatterns =[
	path('', views.PostList.as_view(), name='home'),
	path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
	path("feed/rss", LatestPostsFeed(), name="post_feed"),
	#path('', views.CommentList.as_view(), name='comment-count'),
	#path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
	path('<slug:slug>/', views.post_detail, name='post_detail'),
]