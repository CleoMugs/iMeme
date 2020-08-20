from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    
    path('admin/', admin.site.urls),

    path('', include('iblog.urls')),
    path('accounts/', include('allauth.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('iblog.api.urls')),
    path('avatar/', include('avatar.urls')),
    #path('', TemplateView.as_view(template_name='index.html')), # revisit
]


if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)