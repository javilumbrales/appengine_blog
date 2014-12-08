from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from blog.views import BlogList

urlpatterns = [
            url(r'^$',login_required(BlogList.as_view(template_name='manage.html')), name="list"),
            url(r'^add/$', 'blog.views.add', name="add"),
            url(r'^edit/(?P<pk>[\d]{16,16})/$', 'blog.views.edit', name="edit"),
            url(r'^delete/(?P<pk>[\d]{16,16})/$', 'blog.views.delete', name="delete"),
            url(r'^serve/(?P<pk>[\d]{1,16})/$', 'blog.views.download_handler', name="serve_image"),
            ]