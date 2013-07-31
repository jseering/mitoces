from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'cas_client.views.index', name="root"),

    url(r'^explore/$', 'cas_client.views.explore', name="explore"),

    url(r'^create/$', 'cas_client.views.create', name="create"),

	url(r'^keywords/$', 'cas_client.views.keywords', name="keywords"),
	url(r'^keywords/(?P<keyword_id>\d+)/$', 'cas_client.views.keyword', name="keyword"),

	url(r'^outcomes/$', 'cas_client.views.outcomes', name="outcomes"),
    url(r'^outcomes/(?P<outcome_id>\d+)/$', 'cas_client.views.outcome', name="outcome"),

    url(r'^modules/$', 'cas_client.views.modules', name="modules"),
    url(r'^modules/(?P<module_id>\d+)/$', 'cas_client.views.module', name="module"),

    url(r'^users/$', 'cas_client.views.users', name="users"),
    url(r'^users/(?P<user_id>\d+)/$', 'cas_client.views.user', name="user"),
    url(r'^user/profile/edit/$', 'cas_client.views.edit_profile', name="edit_profile"),

    url(r'^create_name/$', 'cas_client.views.create_name'),
    url(r'^search/$', 'cas_client.views.search'),

    url(r'^cas-test/login/$', 'django_cas.views.login', name="login"),
    url(r'^cas-test/logout/$', 'django_cas.views.logout', name="logout"),

    url(r'^cas-test$', 'cas_client.views.index', name="home"),
)
