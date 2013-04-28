#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from techism.events import event_service
import json
import logging


@require_http_methods(["POST"])
def csp_reporting(request):
  data = json.loads(request.body)
  values = data["csp-report"]
  logger = logging.getLogger(__name__)
  logger.warning('[CSP-REPORT]' + str(values))
  return HttpResponse('')
	

@require_http_methods(["GET"])
def events(request, year, month = None, day = None):
  event_list = event_service.get_event_query_set()
  event_list = event_list.filter(date_time_begin__year=year)
  if month:
    event_list = event_list.filter(date_time_begin__month=month)
  if day:
    event_list = event_list.filter(date_time_begin__day=day)
  events = []
  for event in event_list:
    ev = dict()
    ev['id'] = str(event.id)
    ev['title'] = event.title
    date_time_begin_local = timezone.localtime(event.date_time_begin)
    date_time_begin_str = date_time_begin_local.strftime("%Y-%m-%d %H:%M")
    ev['date_time_begin'] = date_time_begin_str

    date_time_end_local = timezone.localtime(event.date_time_begin)
    date_time_end_str = date_time_end_local.strftime("%Y-%m-%d %H:%M")
    ev['date_time_end'] = date_time_end_str
    ev['url'] = event.url
    ev['description'] = event.description
    ev['canceled'] = event.canceled
    location = event.location
    if location:
      loc = dict()
      loc ['name'] = location.name
      loc ['street'] = location.street
      loc ['city'] = location.city
      loc ['latitude'] = location.latitude
      loc ['longitude'] = location.longitude
      ev['location'] = loc
    events.append(ev)
  events_as_json = json.dumps(events)
  return HttpResponse(events_as_json, mimetype="application/json")


@require_http_methods(["POST"])
def create(request):
  data = json.loads(request.body)
  return HttpResponse('')