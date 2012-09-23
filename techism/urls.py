from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'techism.events.views.index'),
    
    # static pages
    (r'^impressum/$', direct_to_template, { 'template': 'impressum.html' }),
    (r'^about/$', direct_to_template, { 'template': 'about.html' }),

    # Examples:
    # url(r'^$', 'techism.views.home', name='home'),
    # url(r'^techism/', include('techism.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
