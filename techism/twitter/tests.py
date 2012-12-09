#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
import twitter
import mock
from django.conf import settings


class TwitterTest(TestCase):

    fixtures = ['test-utils/fixture.json']
    
    ## Integration Tests

    def test_get_short_term_events(self):
        event_list = twitter.get_short_term_events()
        self.assertEqual(len(event_list), 2)

    ## Unit Tests

    def test_format_tweet(self):
        event = Mock ()
        event.get_number_of_days = mock.Mock(return_value=0)
        now = timezone.localtime(timezone.now())
        now_str = now.strftime("%d.%m.%Y %H:%M")
        event.date_time_begin = now
        event.get_absolute_url = mock.Mock(return_value='/events/java-event-1')
        event.title = 'Testevent'
        tweet = twitter.format_tweet(event, '')
        self.assertEqual(tweet, u'Testevent - ' + now_str + ' ' + settings.HTTP_URL + '/events/java-event-1')



class Mock(object):
    pass
