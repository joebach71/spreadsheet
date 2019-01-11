from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^/?$', views.index, name='index'),
    url(r'^products/(?P<pk>[0-9]+)/save', views.save, name='save'),
    url(r'^products/(?P<pk>[0-9]+)/confirm', views.confirm, name="confirm"),
    url(r'^products/(?P<pk>[0-9]+)/export', views.export_xlsx, name="Export XLSX"),
    url(r'^products/(?P<pk>[0-9]+)/import/confirm', views.confirm_import_data, name="Confirm Import Data"),
    url(r'^products/(?P<pk>[0-9]+)/import/xlsx', views.import_data, name="Import Data"),
    url(r'^products/(?P<pk>[0-9]+)/api/stringid/(?P<stringid>.*)/region/(?P<region>.*)', views.get_languagestring, name="languagestring"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
