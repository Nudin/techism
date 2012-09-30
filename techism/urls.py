from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from techism.rss.feeds import UpcommingEventsRssFeed, UpcommingEventsAtomFeed

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'techism.events.views.index'),
    
    # static pages
    (r'^impressum/$', direct_to_template, { 'template': 'impressum.html' }),
    (r'^about/$', direct_to_template, { 'template': 'about.html' }),
    
    # iCal
    (r'^feed.ics$', 'techism.ical.views.ical'),
    (r'^ical/(?P<event_id>.+).ics$', 'techism.ical.views.ical_single_event'),

    # Atom
    (r'^feeds/atom/upcomming_events$', UpcommingEventsAtomFeed()),
    
    #RSS
    (r'^feeds/rss/upcomming_events$', UpcommingEventsRssFeed()),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
