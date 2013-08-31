from django import forms
from django.db import models

from ophrys.core.models import TaggedModel
from ophrys.utils.models import GetAbsoluteUrlMixin, AutoModelMixin, ExtraFormField


class TestModelA(GetAbsoluteUrlMixin, models.Model):
    name = models.TextField()


class TestModelB(GetAbsoluteUrlMixin, models.Model):
    name = models.TextField()
    slug = models.SlugField()


class TestModelC(AutoModelMixin, models.Model):
    """
    This model is mixed with AutoModelMixin for testing.
    """
    name = models.TextField()


class TestModelD(TaggedModel):
    """
    This model is a tagged model for testing.
    """
    name = models.TextField()


class TestModelE(models.Model):
    """
    This model is to test extra form field functionality.
    """
    name = models.TextField()

    @classmethod
    def get_extra_form_fields(cls):
        """
        Simple test functionality: Give a string to extra field 1 and an
        integer to extra field 2. The string is appended to the name as often
        as the integer value says.
        """
        class ExtraFormFieldOne(ExtraFormField):
            name = 'extra_1'
            form_field = forms.CharField()

            def get_initial(self, instance):
                return instance.name.split('_')[-1] if instance else ''

            def process_field(self, instance, value):
                instance._value = value

        class ExtraFormFieldTwo(ExtraFormField):
            name = 'extra_2'
            form_field = forms.IntegerField()
            initial = 1

            def process_field(self, instance, value):
                suffix = ''
                for i in range(value):
                    suffix += '_' + instance._value
                instance.name += suffix
                instance.save()

        return (ExtraFormFieldOne(), ExtraFormFieldTwo())


class TestModelF_1(models.Model):
    """
    This model is to test extra form field functionality with bad
    implementations.
    """
    @classmethod
    def get_extra_form_fields(cls):
        return [type('ExtraFormFieldOne', (ExtraFormField,), {})()]


class TestModelF_2(models.Model):
    """
    This model is to test extra form field functionality with bad
    implementations.
    """
    @classmethod
    def get_extra_form_fields(cls):
        return [type('ExtraFormFieldOne', (ExtraFormField,), {'name': 'some_name_cogh9meiShi8eikieB4g'})()]


class TestModelF_3(models.Model):
    """
    This model is to test extra form field functionality with bad
    implementations.
    """
    @classmethod
    def get_extra_form_fields(cls):
        return [type('ExtraFormFieldOne',
                     (ExtraFormField,),
                     {'name': 'some_name_leehoovooNien7Va5shi',
                      'form_field': forms.CharField()})()]


from .config import config_group_test_one
"""
Imports the test config variables to connect the relevant signal.
"""
