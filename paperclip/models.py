from __future__ import unicode_literals

import mimetypes
import os

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from embed_video.fields import EmbedVideoField

from paperclip.settings import PAPERCLIP_ENABLE_VIDEO, PAPERCLIP_FILETYPE_MODEL, PAPERCLIP_ENABLE_LINK


@python_2_unicode_compatible
class FileType(models.Model):
    type = models.CharField(max_length=128, verbose_name=_("File type"))

    class Meta:
        abstract = True
        verbose_name = _("File type")
        verbose_name_plural = _("File types")
        ordering = ['type']

    @classmethod
    def objects_for(cls, request):
        # request ignored by default
        return cls.objects.all()

    def __str__(self):
        return self.type


class AttachmentManager(models.Manager):
    def attachments_for_object(self, obj):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id,
                           object_id=obj.id)

    def attachments_for_object_only_type(self, obj, filetype):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id,
                           object_id=obj.id,
                           filetype=filetype)


def attachment_upload(instance, filename):
    """Stores the attachment in a "per module/appname/primary key" folder"""
    name, ext = os.path.splitext(filename)
    renamed = slugify(instance.title or name) + ext
    return 'paperclip/%s/%s/%s' % (
        '%s_%s' % (instance.content_object._meta.app_label,
                   instance.content_object._meta.model_name),
        instance.content_object.pk,
        renamed)


@python_2_unicode_compatible
class Attachment(models.Model):
    objects = AttachmentManager()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    attachment_file = models.FileField(_('File'), blank=True,
                                       upload_to=attachment_upload,
                                       max_length=512)
    if PAPERCLIP_ENABLE_VIDEO:
        attachment_video = EmbedVideoField(_('Video URL'), blank=True)
    if PAPERCLIP_ENABLE_LINK:
        attachment_link = models.URLField(_('Picture URL'), blank=True)
    filetype = models.ForeignKey(PAPERCLIP_FILETYPE_MODEL, verbose_name=_('File type'))

    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name="created_attachments",
                                verbose_name=_('Creator'),
                                help_text=_("User that uploaded"))
    author = models.CharField(blank=True, default='', max_length=128,
                              db_column='auteur', verbose_name=_('Author'),
                              help_text=_("Original creator"))
    title = models.CharField(blank=True, default='', max_length=128,
                             db_column='titre', verbose_name=_(u"Filename"),
                             help_text=_("Renames the file"))
    legend = models.CharField(blank=True, default='', max_length=128,
                              db_column='legende', verbose_name=_(u"Legend"),
                              help_text=_("Details displayed"))
    starred = models.BooleanField(default=False, db_column='marque',
                                  verbose_name=_(u"Starred"),
                                  help_text=_("Mark as starred"))

    date_insert = models.DateTimeField(editable=False, auto_now_add=True,
                                       verbose_name=_("Insertion date"))
    date_update = models.DateTimeField(editable=False, auto_now=True,
                                       verbose_name=_("Update date"))

    class Meta:
        abstract = True
        ordering = ['-date_insert']
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")
        default_permissions = ()
        permissions = (
            ('add_attachment', _('Can add attachments')),
            ('change_attachment', _('Can change attachments')),
            ('delete_attachment', _('Can delete attachments')),
            ('read_attachment', _('Can read attachments')),
            ('delete_attachment_others', _("Can delete others' attachments")),
        )

    def __str__(self):
        return '{} attached {}'.format(
            self.creator.username,
            self.attachment_file.name
        )

    @property
    def filename(self):
        return os.path.split(self.attachment_file.name)[1]

    @property
    def mimetype(self):
        mt = mimetypes.guess_type(self.attachment_file.name, strict=True)[0]
        if mt is None:
            return 'application', 'octet-stream'
        return mt.split('/')

    @property
    def is_image(self):
        return self.mimetype[0].startswith('image')
