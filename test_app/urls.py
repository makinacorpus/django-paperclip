from django.conf.urls import url
from .views import TestView

urlpatterns = [
    url(r'^test_object/(?P<pk>\d+)/', TestView.as_view()),
]
