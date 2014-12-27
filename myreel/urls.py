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
    url(r'^movie/remove/(?P<rt_id>\d+)/$', views.remove_movie, name='remove_movie'),

    url(r'^profile/$', views.profile, name='profile'), # ADD NEW PATTERN!
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    #url(r'^accounts/profile/$', views.profile),
    #(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),    
)
