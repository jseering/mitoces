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
    url(r'^explore_outcome/(?P<outcome>[- \w]+)/$', 'cas_client.views.explore_outcome', name="explore outcome"),
    url(r'^explore_keyword/(?P<keyword>[- \w]+)/$', 'cas_client.views.explore_keyword', name="explore keyword"),

    url(r'^module_id/(?P<module>[- \w]+)/$','cas_client.views.module_id'),
    url(r'^outcome_id/(?P<outcome>[- \w]+)/$','cas_client.views.outcome_id'),
    url(r'^keyword_id/(?P<keyword>[- \w]+)/$','cas_client.views.keyword_id'),

    url(r'^exploresearch/$','cas_client.views.exploresearch'),

    url(r'^module/add/$', 'cas_client.views.create', name="create"),
    url(r'^outcome/add/$', 'cas_client.views.add_outcome', name="add outcome"),
    url(r'^keyword/add/$', 'cas_client.views.add_keyword', name="add keyword"),
    url(r'^keyword/new/$', 'cas_client.views.new_keyword', name="new keyword"),
    url(r'^outcome/new/$', 'cas_client.views.new_outcome', name="new outcome"),

    url(r'^keyword/search/$', 'cas_client.views.keyword_search', name="keyword search"),
    url(r'^outcome/search/$', 'cas_client.views.outcome_search', name="outcome search"),

	url(r'^keywords/$', 'cas_client.views.keywords', name="keywords"),
	url(r'^keywords/(?P<keyword_id>\d+)/$', 'cas_client.views.keyword', name="keyword"),

	url(r'^outcomes/$', 'cas_client.views.outcomes', name="outcomes"),
    url(r'^outcomes/(?P<outcome_id>\d+)/$', 'cas_client.views.outcome', name="outcome"),

    url(r'^modules/$', 'cas_client.views.modules', name="modules"),
    url(r'^modules/(?P<module_id>\d+)/$', 'cas_client.views.module', name="module"),

    url(r'^users/$', 'cas_client.views.users', name="users"),
    url(r'^users/(?P<user_id>\d+)/$', 'cas_client.views.user', name="user"),
    url(r'^user/profile/edit/$', 'cas_client.views.edit_profile', name="edit_profile"),

    url(r'^create_name_keyword/$', 'cas_client.views.create_name_keyword'),
    url(r'^create_name_outcome/$', 'cas_client.views.create_name_outcome'),
    url(r'^create_outcome_keyword/$', 'cas_client.views.create_outcome_keyword'),
    url(r'^search/$', 'cas_client.views.search'),

    url(r'^cas-test/login/$', 'django_cas.views.login', name="login"),
    url(r'^cas-test/logout/$', 'django_cas.views.logout', name="logout"),

    url(r'^cas-test$', 'cas_client.views.index', name="home"),
)
