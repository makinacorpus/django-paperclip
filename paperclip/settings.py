from django.conf import settings

PAPERCLIP_ENABLE_VIDEO = getattr(settings, 'PAPERCLIP_ENABLE_VIDEO', False)
PAPERCLIP_ACTION_HISTORY_ENABLED = getattr(settings, 'PAPERCLIP_ACTION_HISTORY_ENABLED', True)
PAPERCLIP_FILETYPE_MODEL = getattr(settings, 'PAPERCLIP_FILETYPE_MODEL', 'paperclip.FileType')
PAPERCLIP_ATTACHMENT_MODEL = getattr(settings, 'PAPERCLIP_ATTACHMENT_MODEL', 'paperclip.Attachment')
