from django.conf.urls import patterns, include, url
from django.conf import settings

# serve static static in development mode
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
 
# serve media files in development mode
from django.conf.urls.static import static
import os

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('guwen.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^selectable/', include('selectable.urls')),
    url(r'^accounts/', include('auth_frontend.urls')),
)

# local settings only
if os.environ['DJANGO_SETTINGS_MODULE'] == 'django_base.settings':
	# static
	urlpatterns += staticfiles_urlpatterns()
	# media
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
