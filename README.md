# Paperclip

Add attachments to Django models, used in [MapEntity](https://github.com/makinacorpus/django-mapentity).

[![Release status](https://img.shields.io/pypi/v/paperclip.svg)](https://pypi.python.org/pypi/paperclip)
[![CI status](https://github.com/makinacorpus/django-paperclip/actions/workflows/python-package.yml/badge.svg)](https://github.com/makinacorpus/django-paperclip/actions/workflows/python-package.yml)
[![Coverage](https://codecov.io/gh/makinacorpus/django-paperclip/branch/master/graph/badge.svg?token=OB6f944vAt)](https://codecov.io/gh/makinacorpus/django-paperclip)
![Python versions](https://img.shields.io/badge/python-%3E%3D%203.11-blue.svg)
![Django versions](https://img.shields.io/badge/django-%3E%3D%205.2-blue.svg)

---

## Installation

Install from PyPI using `pip`:

```bash
pip install paperclip
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/makinacorpus/django-paperclip.git
```

> **Note:** `paperclip` uses `python-magic` for MIME type validation, which requires `libmagic` to be installed on your system.

---

## Upgrade

After upgrading to `0.4.0`, if you want to enable links to YouTube/SoundCloud media (`PAPERCLIP_ENABLE_VIDEO = True`), add the `attachment_video` column to your database:

```sql
ALTER TABLE paperclip_attachment ADD COLUMN attachment_video VARCHAR(200) NOT NULL DEFAULT '';
```

---

## Basic Usage

1. **Add apps to `INSTALLED_APPS`** in your Django settings:

   ```python
   INSTALLED_APPS = [
       # ...
       'easy_thumbnails',
       'embed_video',
       'paperclip',
   ]
   ```

2. **Include Paperclip URLs** in your root `urls.py`:

   ```python
   from django.urls import include, path

   urlpatterns = [
       # ...
       path('paperclip/', include('paperclip.urls')),
       # ...
   ]
   ```

3. **Include static scripts** in your base template:

   ```html
   <script src="{% static 'paperclip/bootstrap-confirm.js' %}" type="text/javascript"></script>
   <script src="{% static 'paperclip/spin.min.js' %}" type="text/javascript"></script>
   <script src="{% static 'paperclip/paperclip.js' %}" type="text/javascript"></script>
   ```

   If you use Bootstrap 3 or Bootstrap 4, include `paperclip/bootstrap-3-confirm.js` or `paperclip/bootstrap-4-confirm.js` instead of `paperclip/bootstrap-confirm.js`.

4. **Include the attachment list and upload form** in your object detail template:

   ```django
   {% include 'paperclip/attachment_list.html' with object=my_instance attachment_form_next=my_instance.get_detail_url %}
   ```

5. **Define concrete models** in one of your apps (since `FileType`, `License`, and `Attachment` are abstract models):

   ```python
   import paperclip.models


   class FileType(paperclip.models.FileType):
       pass


   class License(paperclip.models.License):
       pass


   class Attachment(paperclip.models.Attachment):
       pass
   ```

6. **Configure required settings** in `settings.py`:

   ```python
   PAPERCLIP_FILETYPE_MODEL = 'myapp.FileType'
   PAPERCLIP_LICENSE_MODEL = 'myapp.License'
   PAPERCLIP_ATTACHMENT_MODEL = 'myapp.Attachment'
   ```

7. **Create and apply migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

## Configuration

### Required Settings

| Setting | Description |
| --- | --- |
| `PAPERCLIP_FILETYPE_MODEL` | Dotted path to your concrete `FileType` model (e.g. `'myapp.FileType'`). |
| `PAPERCLIP_LICENSE_MODEL` | Dotted path to your concrete `License` model (e.g. `'myapp.License'`). |
| `PAPERCLIP_ATTACHMENT_MODEL` | Dotted path to your concrete `Attachment` model (e.g. `'myapp.Attachment'`). |

### Optional Settings

| Setting | Default | Description |
| --- | --- | --- |
| `PAPERCLIP_ENABLE_VIDEO` | `False` | Enable attaching YouTube/SoundCloud video URLs (`attachment_video` field). |
| `PAPERCLIP_ENABLE_LINK` | `False` | Enable attaching external picture URLs (`attachment_link` field). |
| `PAPERCLIP_ACTION_HISTORY_ENABLED` | `True` | Record attachment additions and updates in Django admin `LogEntry`. |
| `PAPERCLIP_RESIZE_ATTACHMENTS_ON_UPLOAD` | `False` | Automatically resize uploaded images (excluding SVGs) to fit within `PAPERCLIP_MAX_ATTACHMENT_WIDTH` × `PAPERCLIP_MAX_ATTACHMENT_HEIGHT`. |
| `PAPERCLIP_MAX_ATTACHMENT_WIDTH` | `1280` | Maximum width (px) when `PAPERCLIP_RESIZE_ATTACHMENTS_ON_UPLOAD` is enabled. |
| `PAPERCLIP_MAX_ATTACHMENT_HEIGHT` | `1280` | Maximum height (px) when `PAPERCLIP_RESIZE_ATTACHMENTS_ON_UPLOAD` is enabled. |
| `PAPERCLIP_MIN_IMAGE_UPLOAD_WIDTH` | `None` | Minimum required width (px) for uploaded images. |
| `PAPERCLIP_MIN_IMAGE_UPLOAD_HEIGHT` | `None` | Minimum required height (px) for uploaded images. |
| `PAPERCLIP_MAX_BYTES_SIZE_IMAGE` | `None` | Maximum allowed file size in bytes for uploaded files. |
| `PAPERCLIP_ALLOWED_EXTENSIONS` | `None` | List/iterable of allowed lowercase file extensions without leading dots (e.g. `['pdf', 'jpg', 'png']`). When set, file extension and actual MIME type (via `python-magic`) are validated. |
| `PAPERCLIP_EXTRA_ALLOWED_MIMETYPES` | `{}` | Mapping of extension to additional allowed MIME types (e.g. `{'geojson': ['application/json']}`). |
| `PAPERCLIP_RANDOM_SUFFIX_SIZE` | `12` | Length of the random alphanumeric suffix appended to stored filenames. |

---

## Permissions

The abstract `Attachment` model disables Django's default permissions (`default_permissions = ()`) and defines the following custom permissions on your concrete `Attachment` model:

- `add_attachment` — Can add attachments
- `change_attachment` — Can change attachments
- `delete_attachment` — Can delete attachments
- `read_attachment` — Can read attachments
- `delete_attachment_others` — Can delete others' attachments

---

## Templates

Three templates are embedded and can easily be overridden in your project:

- `paperclip/attachment_list.html` — Renders the attached files table and the upload form using the two partials below.
- `paperclip/_attachment_table.html` — Renders the table of attached files for an object. You can add extra columns using `{% block extra_column_header %}` and `{% block extra_column_data %}`.
- `paperclip/_attachment_form.html` — Renders the upload/edit attachment form.

---

## Template Tags and Filters

Load the tag library in your templates with:

```django
{% load attachments_tags %}
```

### `get_attachments_for`

Resolves attachments associated with a given object. You can specify the context variable name using `as` (defaults to `attachments`), and optionally filter by a `FileType` instance using `only_type`.

```django
{% get_attachments_for my_instance as "my_attachments" %}
{% get_attachments_for my_instance as "my_attachments" only_type my_filetype_instance %}
```

### `attachment_form`

Renders an "upload attachment" form. The `obj` argument is required and represents the instance to which the file will be associated. A bound form can optionally be passed as the `form` argument.

- `attachment_form_next` is expected in the template context (redirect URL after submission).
- `attachment_form_class` can optionally be set in the context to use a custom form class.

```django
{% with object=my_instance attachment_form_next=my_instance.get_detail_url %}
    {% attachment_form object %}
{% endwith %}
```

Or from a view:

```python
# views.py
context['object'] = my_instance
context['attachment_form_next'] = my_instance.get_detail_url()
context['attachment_form_class'] = MyAttachmentForm
```

```django
{# template #}
{% attachment_form object %}
```

### Filters

- Permission checks on `perms`: `read_attachment`, `add_attachment`, `change_attachment`, `delete_attachment`, `delete_attachment_others` (e.g. `{% if perms|add_attachment %}`).
- `icon_name`: Returns the file extension icon name derived from an attachment's MIME type (falls back to `'bin'`).

---

## Using a Custom Form

You can use a custom Django form (recommended if you use `django-crispy-forms` or `django-floppyforms`):

1. **Subclass `paperclip.forms.AttachmentForm`** so the built-in form logic is preserved:

   ```python
   from paperclip.forms import AttachmentForm


   class MyAttachmentForm(AttachmentForm):
       # ...
       pass
   ```

2. **Pass `attachment_form_class` in your view context**:

   ```python
   context['attachment_form_class'] = MyAttachmentForm
   ```

3. **Override the `add_attachment` and `update_attachment` URLs** in `urls.py` *after* including `paperclip.urls`:

   ```python
   from django.urls import include, path
   from paperclip import views as paperclip_views
   from my_app.forms import MyAttachmentForm

   urlpatterns = [
       path('paperclip/', include('paperclip.urls')),
       # ...
       path(
           'add-for/<str:app_label>/<str:model_name>/<int:pk>/',
           paperclip_views.add_attachment,
           kwargs={'attachment_form': MyAttachmentForm},
           name='add_attachment',
       ),
       path(
           'update/<int:attachment_pk>/',
           paperclip_views.update_attachment,
           kwargs={'attachment_form': MyAttachmentForm},
           name='update_attachment',
       ),
   ]
   ```

---

## Cleanup

Deleting or replacing an attachment does not automatically remove old files from disk. You can periodically clean up obsolete files by running:

```bash
python manage.py clean_attachments
```

Pass `--noinput` to skip the interactive confirmation prompt:

```bash
python manage.py clean_attachments --noinput
```

---

## Development & Testing

Install development dependencies and run the test suite:

```bash
pip install -e .[dev]
python manage.py test
```

Or run with coverage:

```bash
coverage run ./manage.py test
```

---

## Authors

[![Makina Corpus](https://github.com/makinacorpus.png)](https://www.makina-corpus.com)

---

## License

* LGPL (see [LICENSE](LICENSE))
