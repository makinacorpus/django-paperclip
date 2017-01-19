from django.contrib import admin
from paperclip.admin import AttachmentInlines
from paperclip.models import FileType, Attachment
from .models import TestObject


admin.site.register(FileType)
admin.site.register(Attachment)


@admin.register(TestObject)
class TestObjectAdmin(admin.ModelAdmin):
    inlines = [AttachmentInlines]
