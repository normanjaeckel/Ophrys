from django.test import TestCase
from django.test.client import Client

from tests.models import TestModelA, TestModelB, TestModelC, TestModelF_3


class GetAbsoluteUrlMixinTest(TestCase):
    urls = 'tests.urls'

    def test_reverse_list_and_create(self):
        test_object = TestModelA.objects.create()
        self.assertEqual(test_object.get_absolute_url('list'), '/test_model/test_model_a/ohl9pheengooLai0noo1/')

    def test_reverse_via_pk(self):
        test_object = TestModelA.objects.create()
        self.assertEqual(test_object.get_absolute_url(), '/test_model/test_model_a/ahquee1daiQuo7wei0le/1/')
        self.assertEqual(test_object.get_absolute_url(url_name='update'), '/test_model/test_model_a/lahQuo2pheeM0iech7ku/1/')

    def test_reverse_via_slug(self):
        test_object = TestModelB.objects.create(slug='kel7EiMaek2thahf8aoy')
        self.assertEqual(test_object.get_absolute_url(), '/test_model/test_model_b/Udaicae3EiKai8eiveif/kel7EiMaek2thahf8aoy/')
        self.assertEqual(test_object.get_absolute_url(url_name='update'), '/test_model/test_model_b/xoorumi8Thei5ayei5io/kel7EiMaek2thahf8aoy/')


class AutoModelMixinTest(TestCase):
    def test_get_view_class(self):
        test_object = TestModelC.objects.create(name='xoo8aing6iecheizeeDu')
        self.assertRaisesMessage(
            ValueError,
            'The view name "UnknownViewClass_xaa7tooleingaWo0rah8" is unknown.',
            test_object.get_view_class,
            'UnknownViewClass_xaa7tooleingaWo0rah8')


class ExtraFormFieldTest(TestCase):
    urls = 'tests.urls'

    def test_missing_name(self):
        self.assertRaisesMessage(
            NotImplementedError,
            'You either have to provide a name or define a get_name method on your ExtraFormField class.',
            Client().get,
            '/test_model/test_model_f_1/create/')

    def test_missing_form_field(self):
        self.assertRaisesMessage(
            NotImplementedError,
            'You either have to provide a form_field or define a get_form_field method on your ExtraFormField class.',
            Client().get,
            '/test_model/test_model_f_2/create/')

    def test_missing_process_field_method(self):
        TestModelF_3.objects.create()
        self.assertRaisesMessage(
            NotImplementedError,
            "You have to define what should happen with the field's value if the form is valid.",
            Client().post,
            '/test_model/test_model_f_3/1/update/',
            {'some_name_leehoovooNien7Va5shi': 'Oeghohvahpakoh7baeSh'})
