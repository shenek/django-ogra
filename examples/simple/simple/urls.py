from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'simple.views.index', name='index'),
)
