from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^cas-test/admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^cas-test/admin/', include(admin.site.urls)),

    url(r'^$', 'cas-client.views.index', name="root"),

    url(r'^cas-test/login/$', 'django_cas.views.login', name="login"),
    url(r'^cas-test/logout/$', 'django_cas.views.logout', name="logout"),

    url(r'^cas-test$', 'cas-client.views.index', name="home"),
)
