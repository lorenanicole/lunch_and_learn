from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from lunch_and_learn.views import timeline, post_status

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lunch_and_learn.views.home', name='home'),
    url(r'^timeline/', timeline, name='timeline'),
    url(r'^tweet/', post_status, name='post_status'),


    # url(r'^lunch_and_learn/', include('lunch_and_learn.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #
    # # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
