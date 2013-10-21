from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Admin docs:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Admin:
    url(r'^admin/', include(admin.site.urls)),

    # Home
    url(r'^$', 'cas_client.views.index', name="root"),
    
    # Authentication
    url(r'^cas_test/login/$', 'django_cas.views.login', name="login"),
    url(r'^cas_test/logout/$', 'django_cas.views.logout', name="logout"),
    url(r'^cas_test$', 'cas_client.views.index', name="home"),
)
