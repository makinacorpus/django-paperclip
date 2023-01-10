import mimetypes
import magic
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileValidator:
    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and self.message == other.message
        )


class FileMimetypeValidator(FileValidator):
    message = _(
        'File type “%(extension)s” is not allowed. '
        'Allowed types are: %(allowed_extensions)s.'
    )

    def __call__(self, value):
        if settings.PAPERCLIP_ALLOWED_EXTENSIONS is not None:
            value.seek(0)
            file_mimetype = magic.from_buffer(value.read(2048), mime=True).split('/')[1]
            extension = mimetypes.guess_type(value.name, strict=True)[0].split('/')[1].lower()
            if extension not in settings.PAPERCLIP_ALLOWED_EXTENSIONS or file_mimetype not in settings.PAPERCLIP_ALLOWED_EXTENSIONS:
                raise ValidationError(
                    self.message,
                    params={
                        'extension': extension if extension not in settings.PAPERCLIP_ALLOWED_EXTENSIONS else file_mimetype,
                        'allowed_extensions': settings.PAPERCLIP_ALLOWED_EXTENSIONS,
                        'value': value.name,
                    }
                )
