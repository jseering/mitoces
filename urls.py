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

    # Users
    url(r'^users/(?P<user_id>\d+)/$', 'cas_client.views.profile', name="profile"),

    # Home
    url(r'^$', 'cas_client.views.index', name="root"),

    # Module
    url(r'^modules/(?P<module_id>\d+)/$', 'cas_client.views.module', name="module"),
    url(r'^modules/(?P<module_id>\d+)/edit/$', 'cas_client.views.edit_module', name="edit module"),
    url(r'^modules/(?P<module_id>\d+)/delete/$', 'cas_client.views.delete_module', name="delete module"),
    url(r'^modules/(?P<module_id>\d+)/remove/outcome/(?P<outcome_id>\d+)/$', 'cas_client.views.remove_outcome_from_module', name="remove outcome from module"),

    # Outcome
    url(r'^outcomes/(?P<outcome_id>\d+)/$', 'cas_client.views.outcome', name="outcome"),
    url(r'^outcomes/(?P<outcome_id>\d+)/edit/$', 'cas_client.views.edit_outcome', name="edit outcome"),
    url(r'^outcomes/(?P<outcome_id>\d+)/delete/$', 'cas_client.views.delete_outcome', name="delete outcome"),

    # Subject
    url(r'^subjects/(?P<subject_id>\d+)/$', 'cas_client.views.subject', name="subject"),
    url(r'^subjects/(?P<subject_id>\d+)/edit/$', 'cas_client.views.edit_subject', name="edit subject"),
    url(r'^subjects/(?P<subject_id>\d+)/delete/$', 'cas_client.views.delete_subject', name="delete subject"),

    # Department
    url(r'^departments/(?P<department_id>\d+)/$', 'cas_client.views.department', name="department"),

    # Authentication
    url(r'^cas_test/login/$', 'django_cas.views.login', name="login"),
    url(r'^cas_test/logout/$', 'django_cas.views.logout', name="logout"),
    url(r'^cas_test$', 'cas_client.views.index', name="home"),
)
