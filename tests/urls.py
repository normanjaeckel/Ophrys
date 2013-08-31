from django.conf.urls import patterns, include, url

from ophrys.utils.views import CreateView, UpdateView

from tests.models import TestModelC, TestModelE, TestModelF_1, TestModelF_2, TestModelF_3


test_model_a_urlpatterns = patterns(
    '',
    url(r'^ohl9pheengooLai0noo1/', 'some_view', name='list'),
    url(r'^ahquee1daiQuo7wei0le/(?P<pk>\d+)/', 'some_view', name='detail'),
    url(r'^lahQuo2pheeM0iech7ku/(?P<pk>\d+)/', 'some_view', name='update'))


test_model_b_urlpatterns = patterns(
    '',
    url(r'^Udaicae3EiKai8eiveif/(?P<slug>\w+)/', 'some_view', name='detail'),
    url(r'^xoorumi8Thei5ayei5io/(?P<slug>\w+)/', 'some_view', name='update'))


test_model_urlpatterns = patterns(
    '',
    url(r'^test_model_a/', include(test_model_a_urlpatterns, namespace='TestModelA')),
    url(r'^test_model_b/', include(test_model_b_urlpatterns, namespace='TestModelB')),
    url(r'^test_model_c/', include(TestModelC().urls)),
    url(r'^test_model_e/create/', CreateView.as_view(model=TestModelE, success_url='#')),
    url(r'^test_model_e/(?P<pk>\d+)/update/', UpdateView.as_view(model=TestModelE, template_name='tests/test_form_template.html', success_url='#')),
    url(r'^test_model_f_1/create/', CreateView.as_view(model=TestModelF_1)),
    url(r'^test_model_f_2/create/', CreateView.as_view(model=TestModelF_2)),
    url(r'^test_model_f_3/(?P<pk>\d+)/update/', UpdateView.as_view(model=TestModelF_3, success_url='#')))


urlpatterns = patterns(
    '',
    url(r'^test_model/', include(test_model_urlpatterns, namespace='tests')))
