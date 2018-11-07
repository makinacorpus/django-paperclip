from __future__ import unicode_literals

from django.db import models
from paperclip.models import FileType as BaseFileType, Attachment as BaseAttachment
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class TestObject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Filetype(BaseFileType):
    foo = models.CharField(max_length=100)


class Attachment(BaseAttachment):
    foo = models.CharField(max_length=100)
