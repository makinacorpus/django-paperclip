from django.contrib import admin
from paperclip import settings
from paperclip.admin import AttachmentInlines
from .models import TestObject


admin.site.register(settings.get_filetype_model())
admin.site.register(settings.get_license_model())
admin.site.register(settings.get_attachment_model())


@admin.register(TestObject)
class TestObjectAdmin(admin.ModelAdmin):
    inlines = [AttachmentInlines]
