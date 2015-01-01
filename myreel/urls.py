from django.conf.urls import patterns, include, url
from django.contrib import admin

from myreel import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myreel.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),

    url(r'^movie/(?P<rt_id>\d+)/$', views.movie, name='movie'),
    url(r'^movie/add/$', views.add_movie, name='add_movie'),
    url(r'^movie/remove/$', views.remove_movie, name='remove_movie'),
    url(r'^movie/search/$', views.search, name='search'),

    # django-allauth
    url(r'^accounts/', include('allauth.urls')),

    url(r'^profile/$', views.profile, name='profile'), # ADD NEW PATTERN!

    url(r'^logout/$', views.user_logout, name='logout'),    
)
