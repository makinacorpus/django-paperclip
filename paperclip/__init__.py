from django.conf import settings

__version__ = "0.3.0"

app_settings = dict({
    'FILETYPE_MODEL': 'FileType',
    'ATTACHMENT_TABLE_NAME': 'paperclip_attachment',
    'ACTION_HISTORY_ENABLED': True
}, **getattr(settings, 'PAPERCLIP_CONFIG', {}))
