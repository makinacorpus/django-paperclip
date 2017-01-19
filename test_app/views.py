from django.views.generic import DetailView
from .models import TestObject


class TestView(DetailView):
    model = TestObject
