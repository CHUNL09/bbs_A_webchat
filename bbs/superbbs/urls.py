"""bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from superbbs import views

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^category/(\d+)/$', views.category,name='category'),
    url(r'^article/(\d+)/$', views.view_article,name='article_details'),
    url(r'^add_comment/$', views.add_comment,name='add_comment'),
    url(r'^add_article/$', views.add_article,name='add_article'),
    url(r'^login', views.mylogin,name='login'),
    url(r'^logout', views.mylogout,name='logout'),

]
