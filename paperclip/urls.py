from django.conf.urls import patterns, url
from paperclip import views

urlpatterns = patterns(
    '',
    url(r'^add-for/(?P<app_label>[\w\-]+)/'
        r'(?P<model_name>[\w\-]+)/(?P<pk>\d+)/$',
        views.add_attachment,
        name="add_attachment"),
    url(r'^update/(?P<attachment_pk>\d+)/$',
        views.update_attachment,
        name="update_attachment"),
    url(r'^delete/(?P<attachment_pk>\d+)/$',
        views.delete_attachment,
        name="delete_attachment"),
    url(r'^star/(?P<attachment_pk>\d+)/$',
        views.star_attachment,
        name="star_attachment"),
    url(r'^get/(?P<app_label>[\w\-]+)/(?P<model_name>[\w\-]+)/(?P<pk>\d+)/$',
        views.get_attachments,
        name="get_attachments"),
)
