from django.urls import path

from test_project.test_app.forms import TestAttachmentForm
from .views import TestView
from paperclip.views import add_attachment

urlpatterns = [
    path('test_object/<int:pk>/', TestView.as_view(), kwargs={'attachment_form': TestAttachmentForm}),
    path('paperclip/add-with-redirect/<str:app_label>/<str:model_name>/<int:pk>/',
         add_attachment, kwargs={'attachment_form': TestAttachmentForm}, name="extra_add_attachment"),
]
