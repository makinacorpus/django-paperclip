from django.conf import settings


app_settings = dict({
    'FILETYPE_MODEL': None,
    'ATTACHMENT_TABLE_NAME': 'paperclip_attachment',
}, **getattr(settings, 'PAPERCLIP_CONFIG', {}))
