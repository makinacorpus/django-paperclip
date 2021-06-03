from django.db import models
from paperclip.models import FileType as BaseFileType, Attachment as BaseAttachment


class TestObject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Filetype(BaseFileType):
    foo = models.CharField(max_length=100)


class Attachment(BaseAttachment):
    foo = models.CharField(max_length=100)
