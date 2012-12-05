#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from techism.events import event_service
from techism.events.forms import EventForm
from techism.models import Event, EventTag, Location
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import html
import json

def index(request):
    event_list = event_service.get_upcomming_published_events_query_set().order_by('date_time_begin').prefetch_related('tags').select_related('location')
    tags = event_service.get_current_tags()
    return render_to_response(
        'events/index.html',
        {
            'event_list': event_list,
            'tags': tags,
            'hostname': request.get_host()
        },
        context_instance=RequestContext(request))

def details(request, event_id):
    # the event_id may be the slugified, e.g. 'munichjs-meetup-286002'
    splitted_event_id = event_id.rsplit('-', 1)
    if len(splitted_event_id) > 1:
        event_id = splitted_event_id[1]
    
    tags = event_service.get_current_tags()
    event = get_object_or_404(Event, id=event_id)
    return render_to_response(
        'events/details.html',
        {
            'event': event,
            'tags': tags,
            'hostname': request.get_host()
        },
        context_instance=RequestContext(request))

def tag(request, tag_name):
    tag = get_object_or_404(EventTag, name=tag_name)
    event_list = event_service.get_upcomming_published_events_query_set().filter(tags=tag).order_by('date_time_begin')
    tags = event_service.get_current_tags()
    return render_to_response(
        'events/index.html', 
        {
            'event_list': event_list, 
            'tags': tags, 
            'tag_name': tag_name
        }, 
        context_instance=RequestContext(request))


def create(request, event_id=None):
    mode = 'CREATE'
    
    if request.method == 'POST':
        return __save_event(request, mode)
    
    form = EventForm()
#    if event_id:
#        event = Event.objects.get(id=event_id)
#        form = __to_event_form(event)
    
    return render_to_response(
        'events/create.html',
        {
            'form': form,
            'mode': mode
        },
        context_instance=RequestContext(request))
    
    
def __save_event(request, mode, old_event=None):
    form = EventForm(request.POST) 
    if form.is_valid(): 
        event= __create_or_update_event_with_location(form, request.user, old_event)
        # TODO: send mail
        #if not event.published:
            #service.send_event_review_mail(event)
        url = event.get_absolute_url()
        return HttpResponseRedirect(url)
    else:
        return render_to_response(
            'events/create.html',
            {
                'form': form, 
                'error': form.errors,
                'mode': mode
            },
            context_instance=RequestContext(request))


def __create_or_update_event_with_location (form, user, event):
    "Creates or updates an Event from the submitted EventForm. If the given Event is None a new Event is created."
    if event == None:
        event = Event()
    
    event.title = form.cleaned_data['title']
    event.date_time_begin = form.cleaned_data['date_time_begin']
    event.date_time_end = form.cleaned_data['date_time_end']
    event.url = form.cleaned_data['url']
    event.description = form.cleaned_data['description']
    event.location = form.cleaned_data['location']
    
    #if event.location == None:
    #    location = __create_location(form)
    #    event.location=location
    
    # Only when a new event is created
    if event.id == None:
        # auto-publish for staff users
        event.published = user.is_staff
        # link event to user
        if user.is_authenticated():
            event.user = user
    
    # Event must be persisted before tags can be set (many-to-may relationship)
    if event.id == None:
        event.save()
    
    event.tags = form.cleaned_data['tags']
    event.save()
    
    return event

def locations(request):
    return HttpResponse(__get_locations_as_json())

def __get_locations_as_json():
    location_list = Location.objects.all()
    locations = []
    for location in location_list:
        loc = dict()
        loc['id'] = html.escape(location.id)
        loc['name'] = html.escape(location.name)
        loc['street'] = html.escape(location.street)
        loc['city'] = html.escape(location.city)
        loc['latitude'] = html.escape(location.latitude)
        loc['longitude'] = html.escape(location.longitude)
        locations.append(loc)
    locations_as_json = json.dumps(locations)
    return locations_as_json
