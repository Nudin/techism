#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism.models import Event, EventTag, EventChangeLog, Location, Organization, OrganizationTag
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ['published', 'archived']
    list_display = ['title', 'date_time_begin', 'date_time_end', 'location', 'user', 'archived', 'published']

class EventTagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']
    
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'url']

class OrganizationTagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']
    
    
admin.site.register(Event, EventAdmin)
admin.site.register(EventTag, EventTagAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationTag, OrganizationTagAdmin)