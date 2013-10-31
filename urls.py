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
    url(r'^modules/(?P<module_id>\d+)/remove/instructor/(?P<instructor_id>\d+)/$', 'cas_client.views.remove_instructor_from_module', name="remove instructor from module"),
    url(r'^modules/(?P<module_id>\d+)/editname/$', 'cas_client.views.edit_module_name', name="edit module name"),
    url(r'^modules/add/$', 'cas_client.views.add_module', name="add module"),
    url(r'^modules/(?P<module_id>\d+)/editdescription/$', 'cas_client.views.edit_module_description', name="edit module description"),
    url(r'^modules/(?P<module_id>\d+)/add/outcome/$', 'cas_client.views.add_outcome_to_module', name="add outcome to module"),
    url(r'^modules/(?P<module_id>\d+)/add/instructor/$', 'cas_client.views.add_instructor_to_module', name="add instructor to module"),
    url(r'^modules/(?P<module_id>\d+)/add/outcome/(?P<outcome_id>\d+)/$', 'cas_client.views.add_existing_outcome_to_module', name="add existing outcome to module"),

    # Outcome
    url(r'^outcomes/(?P<outcome_id>\d+)/$', 'cas_client.views.outcome', name="outcome"),
    url(r'^outcomes/(?P<outcome_id>\d+)/edit/$', 'cas_client.views.edit_outcome', name="edit outcome"),
    url(r'^outcomes/(?P<outcome_id>\d+)/delete/$', 'cas_client.views.delete_outcome', name="delete outcome"),
    url(r'^outcomes/(?P<outcome_id>\d+)/remove/outcome/(?P<prereq_id>\d+)/$', 'cas_client.views.remove_prereq_from_outcome', name="remove prereq from outcome"),
    url(r'^outcomes/(?P<outcome_id>\d+)/remove/module/(?P<module_id>\d+)/$', 'cas_client.views.remove_outcome_from_module', name="remove module from outcome"),  # this is the same as "remove outcome from module" under Module above
    url(r'^outcomes/(?P<outcome_id>\d+)/remove/subject/(?P<subject_id>\d+)/$', 'cas_client.views.remove_subject_from_outcome', name="remove subject from outcome"),  
    url(r'^outcomes/(?P<outcome_id>\d+)/remove/instructor/(?P<instructor_id>\d+)/$', 'cas_client.views.remove_instructor_from_outcome', name="remove instructor from outcome"),  
    url(r'^outcomes/(?P<outcome_id>\d+)/editname/$', 'cas_client.views.edit_outcome_name', name="edit outcome name"),
    url(r'^outcomes/(?P<outcome_id>\d+)/editdescription/$', 'cas_client.views.edit_outcome_description', name="edit outcome description"),
    url(r'^outcomes/(?P<outcome_id>\d+)/add/instructor/$', 'cas_client.views.add_instructor_to_outcome', name="add instructor to outcome"),
    url(r'^outcomes/(?P<outcome_id>\d+)/get/description/$', 'cas_client.views.get_description_of_outcome', name="get description of outcome"),

    # Subject
    url(r'^subjects/(?P<subject_id>\d+)/$', 'cas_client.views.subject', name="subject"),
    url(r'^subjects/(?P<subject_id>\d+)/edit/$', 'cas_client.views.edit_subject', name="edit subject"),
    url(r'^subjects/(?P<subject_id>\d+)/delete/$', 'cas_client.views.delete_subject', name="delete subject"),
    url(r'^subjects/(?P<subject_id>\d+)/add/instructor/$', 'cas_client.views.add_instructor_to_subject', name="add instructor to subject"),
    url(r'^subjects/(?P<subject_id>\d+)/remove/instructor/(?P<instructor_id>\d+)/$', 'cas_client.views.remove_instructor_from_subject', name="remove instructor from subject"),  

    # Department
    url(r'^departments/(?P<department_id>\d+)/$', 'cas_client.views.department', name="department"),

    # Authentication
    url(r'^cas_test/login/$', 'django_cas.views.login', name="login"),
    url(r'^cas_test/logout/$', 'django_cas.views.logout', name="logout"),
    url(r'^cas_test$', 'cas_client.views.index', name="home"),
)
