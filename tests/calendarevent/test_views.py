import datetime

from django.test import TestCase
from django.test.client import Client
from django.utils.timezone import now, utc

from ophrys.calendarevent.models import Event
from ophrys.core.models import Tag


class CalendarTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_calendar_view_default(self):
        event_1 = Event.objects.create(title='ohP3thu9aiviepaeFeph', begin=now())
        event_2 = Event.objects.create(title='Queiv1oojuLuip9Wo0qu', begin=now()-datetime.timedelta(days=31))
        response = self.client.get('/calendar/')
        self.assertContains(response, '<a href="/calendar/event/1/">ohP3thu9aiviepaeFeph</a>')
        self.assertNotContains(response, '<a href="/calendar/event/2/">Queiv1oojuLuip9Wo0qu</a>')

    def test_calendar_view_specific(self):
        event_1 = Event.objects.create(title='Oochai4aigohheiXohpe', begin=now())
        event_2 = Event.objects.create(title='ahba2Ahzee5Ochohth8u', begin=datetime.datetime(2013, 7, 20, tzinfo=utc))
        response = self.client.get('/calendar/2013-7/')
        self.assertNotContains(response, '<a href="/calendar/event/1/">Oochai4aigohheiXohpe</a>')
        self.assertContains(response, '<a href="/calendar/event/2/">ahba2Ahzee5Ochohth8u</a>')

    def test_calender_view_first_of_month(self):
        event = Event.objects.create(title='looCethie3eech0loayu', begin=datetime.datetime(2013, 11, 30, 23, 59, tzinfo=utc))
        # Default: TIME_ZONE='Europe/Berlin'
        response = self.client.get('/calendar/2013-12/')
        self.assertContains(response, '1 <a href="/calendar/event/1/">looCethie3eech0loayu</a>')
        # Custom: TIME_ZONE='Europe/London'
        with self.settings(TIME_ZONE='Europe/London'):
            response = self.client.get('/calendar/2013-11/')
            self.assertContains(response, '30 <a href="/calendar/event/1/">looCethie3eech0loayu</a>')


class EventTest(TestCase):
    def setUP(self):
        self.client = Client()

    def test_create_view(self):
        response = self.client.get('/calendar/event/create/')
        self.assertTemplateUsed(response, 'calendarevent/event_form.html')
        response = self.client.post('/calendar/event/create/',
                                    {'title': 'ieDie0oow9cho1raem9o',
                                     'begin': now().strftime('%Y-%m-%d %H:%M')})
        self.assertRedirects(response, '/calendar/event/1/')
        self.assertTrue(Event.objects.filter(title='ieDie0oow9cho1raem9o').exists())

    def test_detail_view(self):
        Event.objects.create(title='ohngie5eem1YeeThieve', begin=now())
        response = self.client.get('/calendar/event/1/')
        self.assertContains(response, 'ohngie5eem1YeeThieve')

    def test_update_view(self):
        Event.objects.create(title='Jahxoojauthi3eik8iw6', begin=now())
        response = self.client.get('/calendar/event/1/update/')
        self.assertTemplateUsed(response, 'calendarevent/event_form.html')
        response = self.client.post('/calendar/event/1/update/',
                                    {'title': 'eeQuaingeeshaeshaiG4',
                                     'begin': now().strftime('%Y-%m-%d %H:%M')})
        self.assertRedirects(response, '/calendar/event/1/')
        self.assertTrue(Event.objects.filter(title='eeQuaingeeshaeshaiG4').exists())

    def test_delete_view(self):
        Event.objects.create(title='ohW9eidie7Uatoot9eem', begin=now())
        self.assertTrue(Event.objects.filter(title='ohW9eidie7Uatoot9eem').exists())
        response = self.client.get('/calendar/event/1/delete/')
        self.assertTemplateUsed(response, 'calendarevent/event_confirm_delete.html')
        response = self.client.post('/calendar/event/1/delete/')
        self.assertRedirects(response, '/calendar/event/')
        self.assertFalse(Event.objects.filter(title='ohW9eidie7Uatoot9eem').exists())

    def test_create_with_tags(self):
        tag = Tag.objects.create(name='Ohpaiyae3weingeiThai')
        response = self.client.post('/calendar/event/create/',
                                    {'title': 'amihaeseiMoh1ieTaiwa',
                                     'begin': now().strftime('%Y-%m-%d %H:%M'),
                                     'tags': 'amihaeseiMoh1ieTaiwa Ohpaiyae3weingeiThai'})
        self.assertRedirects(response, '/calendar/event/1/')
        event = Event.objects.get(title='amihaeseiMoh1ieTaiwa')
        self.assertTrue(tag in event.get_tags())
        self.assertTrue(Tag.objects.get(name='amihaeseiMoh1ieTaiwa') in event.get_tags())
        self.assertEqual(Tag.objects.all().count(), 2)

    def test_update_with_tags(self):
        tag_1 = Tag.objects.create(name='voa8TeiYaixiepohsh8o')
        tag_2 = Tag.objects.create(name='eeFaithohw6Vie7Ubuma')
        tag_3 = Tag.objects.create(name='chie6Ailaenoh1Loh6ae')
        event = Event.objects.create(title='Phahzuojie7ene9hei2U', begin=now())
        event.add_tag(tag_1)
        event.add_tag(tag_2)
        self.assertTrue(tag_1 in event.get_tags())
        self.assertTrue(tag_2 in event.get_tags())
        self.assertFalse(tag_3 in event.get_tags())
        response = self.client.post('/calendar/event/1/update/',
                                    {'title': 'Ofaiphiqu0eeHeeheich',
                                     'begin': now().strftime('%Y-%m-%d %H:%M'),
                                     'tags': 'eeFaithohw6Vie7Ubuma chie6Ailaenoh1Loh6ae'})
        self.assertRedirects(response, '/calendar/event/1/')
        event = Event.objects.get(title='Ofaiphiqu0eeHeeheich')
        self.assertFalse(tag_1 in event.get_tags())
        self.assertTrue(tag_2 in event.get_tags())
        self.assertTrue(tag_3 in event.get_tags())
