from django.template import TemplateDoesNotExist
from django.test import TestCase
from django.test.client import Client

from tests.models import TestModelC, TestModelE


class AutoModelMixinViewsTest(TestCase):
    urls = 'tests.urls'

    def setUp(self):
        self.client = Client()

    def test_list_view(self):
        self.assertRaisesMessage(TemplateDoesNotExist, 'tests/testmodelc_list.html', self.client.get, '/test_model/test_model_c/')

    def test_create_view(self):
        self.assertRaisesMessage(TemplateDoesNotExist, 'tests/testmodelc_form.html', self.client.get, '/test_model/test_model_c/create/')
        response = self.client.post('/test_model/test_model_c/create/', {'name': 'aar7iNgou2viw4ahv2ve'})
        self.assertEqual(response.url, 'http://testserver/test_model/test_model_c/1/')
        self.assertTrue(TestModelC.objects.filter(name='aar7iNgou2viw4ahv2ve').exists())

    def test_detail_view(self):
        TestModelC.objects.create(name='AiwaiB5oheez1UJajeip')
        self.assertRaisesMessage(TemplateDoesNotExist, 'tests/testmodelc_detail.html', self.client.get, '/test_model/test_model_c/1/')

    def test_update_view(self):
        TestModelC.objects.create(name='Luph3tohquoesai2haLa')
        self.assertRaisesMessage(TemplateDoesNotExist, 'tests/testmodelc_form.html', self.client.get, '/test_model/test_model_c/1/update/')
        response = self.client.post('/test_model/test_model_c/1/update/', {'name': 'apeej7eiGhab3eipheem'})
        self.assertEqual(response.url, 'http://testserver/test_model/test_model_c/1/')
        self.assertFalse(TestModelC.objects.filter(name='Luph3tohquoesai2haLa').exists())
        self.assertTrue(TestModelC.objects.filter(name='apeej7eiGhab3eipheem').exists())

    def test_delete_view(self):
        TestModelC.objects.create(name='Zah6ceiGiu0ahf7ouH4h')
        self.assertTrue(TestModelC.objects.filter(name='Zah6ceiGiu0ahf7ouH4h').exists())
        self.assertRaisesMessage(TemplateDoesNotExist, 'tests/testmodelc_confirm_delete.html', self.client.get, '/test_model/test_model_c/1/delete/')
        response = self.client.post('/test_model/test_model_c/1/delete/', {})
        self.assertEqual(response.url, 'http://testserver/test_model/test_model_c/')
        self.assertFalse(TestModelC.objects.filter(name='Zah6ceiGiu0ahf7ouH4h').exists())


class ExtraFormFieldTest(TestCase):
    urls = 'tests.urls'

    def setUp(self):
        self.client = Client()

    def test_create_view(self):
        self.assertFalse(TestModelE.objects.exists())
        response = self.client.post(
            '/test_model/test_model_e/create/',
            {'name': 'GaaTooghi9ieMu2oopha', 'extra_1': 'gooxeeVaedee5ahGh0ac', 'extra_2': 2})
        self.assertTrue(TestModelE.objects.filter(name='GaaTooghi9ieMu2oopha_gooxeeVaedee5ahGh0ac_gooxeeVaedee5ahGh0ac').exists())

    def test_update_view_get(self):
        model_object = TestModelE.objects.create(name='gah6eiPh3aeFohnaeNga_aiqu9gainae1Dei1jahf')
        self.assertEqual(model_object.pk, 1)
        response = self.client.get('/test_model/test_model_e/1/update/')
        self.assertContains(
            response,
            '<input id="id_extra_1" name="extra_1" type="text" value="aiqu9gainae1Dei1jahf" />')
        self.assertContains(
            response,
            '<input id="id_extra_2" name="extra_2" type="number" value="1" />')

    def test_update_view_post(self):
        model_object = TestModelE.objects.create(name='ooL3iepai2beev6Noh0a')
        self.assertEqual(model_object.pk, 1)
        response = self.client.post(
            '/test_model/test_model_e/1/update/',
            {'name': 'giengeeTee1ahkeegh0u', 'extra_1': 'AYootheusishai3oiNgo', 'extra_2': 1})
        self.assertTrue(TestModelE.objects.filter(name='giengeeTee1ahkeegh0u_AYootheusishai3oiNgo').exists())
