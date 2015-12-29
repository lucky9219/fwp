"""django_bookmarks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.views.generic import TemplateView
from django.conf.urls import include, url
from django.contrib import admin
from bookmarks.feeds import *



import os.path
feeds={'recent':RecentBookmarks}
urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
#browsing
    url(r'^$','bookmarks.views.main_page'),
    url(r'^user/(\w+)/$','bookmarks.views.user_page',),
    url(r'^popular/$','bookmarks.views.popular_page'),
#session management    
    url(r'^login/$','django.contrib.auth.views.login',),
    url(r'^logout/$','bookmarks.views.logout_page',),
    url(r'^register/$','bookmarks.views.register_page',),
    url(r'^register/success',TemplateView.as_view(template_name="registration/register_success.html")),
#acc management
    url(r'^save/$','bookmarks.views.bookmark_save_page',),
    url(r'^tag/([^\s]+)/$','bookmarks.views.tag_page'),
    url(r'^tag/$','bookmarks.views.tag_cloud_page'),
    url(r'^search/$','bookmarks.views.search_page'),
    url(r'^accounts/login/$','django.contrib.auth.views.login',),
    url(r'^^vote/$', 'bookmarks.views.bookmark_vote_page'),
]