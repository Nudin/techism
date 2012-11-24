"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import timezone
import datetime
from techism.models import Event


class FeedTest(TestCase):
    
    fixtures = ['test-utils/fixture.json']
    now_local = timezone.localtime(timezone.now())
    tomorrow_local = now_local + datetime.timedelta(days=1)
    tomorrow_190000 = tomorrow_local.replace(hour=19, minute=0, second=0)
    tomorrow_localtime = tomorrow_190000.strftime("%d.%m.%Y %H:%M")

    def test_rss_upcomming_events(self):
        event = Event.objects.get(id=1)
        response = self.client.get('/feeds/rss/upcomming_events')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/rss+xml; charset=utf-8')
        self.assertIn("<rss xmlns:atom=\"http://www.w3.org/2005/Atom\" version=\"2.0\">", response.content)
        self.assertEqual(response.content.count("<item>"), 2)
        self.assertIn("<title>Java Event - %s</title>" % self.tomorrow_localtime, response.content)
        self.assertIn("<link>http://testserver%s</link>" % event.get_absolute_url(), response.content)
        self.assertIn("<guid>http://testserver%s</guid>" % event.get_absolute_url(), response.content)

    def test_atom_upcomming_events(self):
        event = Event.objects.get(id=1)
        response = self.client.get('/feeds/atom/upcomming_events')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/atom+xml; charset=utf-8')
        self.assertIn("<feed xmlns=\"http://www.w3.org/2005/Atom\" xml:lang=\"de-DE\">", response.content)
        self.assertEqual(response.content.count("<entry>"), 2)
        self.assertIn("<title>Java Event - %s</title>" % self.tomorrow_localtime, response.content)
        self.assertIn("<link href=\"http://testserver%s\" rel=\"alternate\"></link>" % event.get_absolute_url(), response.content)
        self.assertIn("<id>http://testserver%s</id>" % event.get_absolute_url(), response.content)

