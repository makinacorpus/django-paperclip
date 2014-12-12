from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


app_settings = dict({
    'FILETYPE_MODEL': 'FileType',
    'ATTACHMENT_TABLE_NAME': 'paperclip_attachment',
    'ACTION_HISTORY_ENABLED': True,
    'USE_CRISPY_FORMS': True
}, **getattr(settings, 'PAPERCLIP_CONFIG', {}))

if app_settings['USE_CRISPY_FORMS']:
    try:
        import crispy_forms
    except ImportError:
        raise ImproperlyConfigured(
            "Please install django_crispy_forms or "
            "set USE_CRISPY_FORMS to False in your PAPERCLIP_CONFIG setting.")
