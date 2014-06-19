from django.conf.urls import *
from .views import (add_attachment, delete_attachment,
                    ajax_validate_attachment, get_attachments)

urlpatterns = patterns('',
    url(r'^add-for/(?P<app_label>[\w\-]+)/(?P<module_name>[\w\-]+)/(?P<pk>\d+)/$', add_attachment, name="add_attachment"),
    url(r'^delete/(?P<attachment_pk>\d+)/$', delete_attachment, name="delete_attachment"),
    url(r'^ajax_validate/$', ajax_validate_attachment, name="ajax_validate_attachment"),
    url(r'^get/(?P<app_label>[\w\-]+)/(?P<module_name>[\w\-]+)/(?P<pk>\d+)/$', get_attachments, name="get_attachments"),
)
