from django.db import models
from paperclip.models import FileType, Attachment


class TestObject(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class TestFiletype(FileType):
    foo = models.CharField(max_length=100)


class TestAttachment(Attachment):
    foo = models.CharField(max_length=100)
