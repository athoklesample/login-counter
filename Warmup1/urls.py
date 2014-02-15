from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Warmup1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'login_counter.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('login_counter.urls')),
    url(r'^TESTAPI/', include('login_counter.urls')),

)
