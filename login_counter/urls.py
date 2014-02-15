from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('login_counter.UsersController',
    # Examples:
    # url(r'^$', 'Warmup1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login', 'do_POST'),
    url(r'^add', 'do_POST'),

)

urlpatterns += patterns('login_counter.TESTAPI_Controller',
    url(r'^resetFixture', 'do_POST'),
    url(r'^unitTests', 'do_POST'),
)

urlpatterns += patterns('',
# Examples:
    # url(r'^$', 'Warmup1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

)
