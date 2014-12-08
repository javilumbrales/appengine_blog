from django.conf.urls import *
from django.contrib import admin
import dbindexer

from blog import urls
from blog.views import BlogList

handler500 = 'djangotoolbox.errorviews.server_error'

# django admin
admin.autodiscover()

# search for dbindexes.py in all INSTALLED_APPS and load them
dbindexer.autodiscover()

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    url('^$', BlogList.as_view(template_name='home.html'), name='home'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    ('^manage/', include(urls)),
    ('^admin/', include(admin.site.urls)),
)
