from django.conf import settings

__version__ = "1.0.0"

app_settings = dict({
    'ENABLE_VIDEO': False,
    'FILETYPE_MODEL': 'FileType',
    'ATTACHMENT_TABLE_NAME': 'paperclip_attachment',
    'ACTION_HISTORY_ENABLED': True
}, **getattr(settings, 'PAPERCLIP_CONFIG', {}))
