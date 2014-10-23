from django.conf.urls import *
from .views import (add_attachment, update_attachment, delete_attachment, star_attachment,
                    get_attachments)

urlpatterns = patterns('',
    url(r'^add-for/(?P<app_label>[\w\-]+)/(?P<module_name>[\w\-]+)/(?P<pk>\d+)/$', add_attachment, name="add_attachment"),
    url(r'^update/(?P<attachment_pk>\d+)/$', update_attachment, name="update_attachment"),
    url(r'^delete/(?P<attachment_pk>\d+)/$', delete_attachment, name="delete_attachment"),
    url(r'^star/(?P<attachment_pk>\d+)/$', star_attachment, name="star_attachment"),
    url(r'^get/(?P<app_label>[\w\-]+)/(?P<module_name>[\w\-]+)/(?P<pk>\d+)/$', get_attachments, name="get_attachments"),
)
