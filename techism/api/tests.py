from django.test import TestCase
from django.utils import timezone
import json

class ApiViewTest(TestCase):

    fixtures = ['test-utils/fixture.json']

    def test_csp_reporting(self):
        json_data = '''{"csp-report": {
            "document-uri": "http://example.com/signup.html",
            "referrer": "http://evil.example.net/haxor.html",
            "blocked-uri": "http://evil.example.net/injected.png",
            "violated-directive": "img-src *.example.com",
            "original-policy": "default-src 'self'; img-src 'self' *.example.com; report-uri /_/csp-reports"
                }
            }''';
        response = self.client.post('/api/csp/', json_data, content_type="application/json")
        self.assertEqual('', response.content)

    def test_get_year(self):
        current_year = str(timezone.localtime(timezone.now()).year)
        url = '/api/events/' + current_year + '/'
        response = self.__get_response(url)
        data = json.loads(response.content)
        self.assertEqual(5, len(data))

    def test_get_month(self):
        current_year = str(timezone.localtime(timezone.now()).year)
        current_month = str(timezone.localtime(timezone.now()).month)
        url = '/api/events/' + current_year + '/' + current_month + '/'
        response = self.__get_response(url)
        data = json.loads(response.content)
        self.assertEqual(5, len(data))

    def test_get_day(self):
        current_year = str(timezone.localtime(timezone.now()).year)
        current_month = str(timezone.localtime(timezone.now()).month)
        current_day = str(timezone.localtime(timezone.now()).day)
        url = '/api/events/' + current_year + '/' + current_month + '/' + current_day + '/'
        response = self.__get_response(url)
        data = json.loads(response.content)
        self.assertEqual(2, len(data))

    def test_create_unauthenticated(self):
        json = '''[{ "description": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy...", 
        "title": "Running event without end date", "url": "http://example.com", 
        "canceled": false, "date_time_end": "2013-04-28 17:04", "date_time_begin": "2013-04-28 17:04"}]'''
        response = self.client.post('/api/events/', json, content_type="application/json")
        # TODO: should be 401
        self.assertEqual(response.status_code, 302)
        self.assertIn('accounts/login/?next=/api/events/', response['location'])

    def __get_response(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        return response
