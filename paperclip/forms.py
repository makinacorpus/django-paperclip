from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from paperclip import settings

MODE_CHOICED = [('File', _('File')), ]


class AttachmentForm(forms.ModelForm):
    if settings.PAPERCLIP_ENABLE_VIDEO:
        MODE_CHOICED.append(('Youtube', _('Youtube/Soundcloud URL')))

    if settings.PAPERCLIP_ENABLE_LINK:
        MODE_CHOICED.append(('Link', _('External picture link')))

    if settings.PAPERCLIP_ENABLE_VIDEO or settings.PAPERCLIP_ENABLE_LINK:
        embed = forms.TypedChoiceField(
            label=_(u"Mode"),
            choices=MODE_CHOICED,
            widget=forms.RadioSelect(), initial=False)
    next = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = settings.get_attachment_model()
        if settings.PAPERCLIP_ENABLE_VIDEO and not settings.PAPERCLIP_ENABLE_LINK:
            fields = ('embed', 'attachment_file', 'attachment_video',
                      'filetype', 'author', 'title', 'legend')
        elif settings.PAPERCLIP_ENABLE_VIDEO and settings.PAPERCLIP_ENABLE_LINK:
            fields = ('embed', 'attachment_file', 'attachment_video', 'attachment_link',
                      'filetype', 'author', 'title', 'legend')
        elif settings.PAPERCLIP_ENABLE_LINK and not settings.PAPERCLIP_ENABLE_VIDEO:
            fields = ('embed', 'attachment_file', 'attachment_link',
                      'filetype', 'author', 'title', 'legend')
        else:
            fields = ('attachment_file', 'filetype', 'author', 'title',
                      'legend')

    def __init__(self, request, *args, **kwargs):
        self._object = kwargs.pop('object', None)
        next_url = kwargs.pop('next_url', None)

        super().__init__(*args, **kwargs)
        self.fields['legend'].widget.attrs['placeholder'] = _('Sunset on lake')

        # Allow to override filetype choices
        filetype_model = self.fields['filetype'].queryset.model
        self.fields['filetype'].queryset = filetype_model.objects_for(request)

        # Detect fields errors without uploading (using HTML5)
        self.fields['filetype'].widget.attrs['required'] = 'required'
        self.fields['author'].widget.attrs['pattern'] = r'^\S.*'
        self.fields['legend'].widget.attrs['pattern'] = r'^\S.*'

        self.fields['attachment_file'].widget = forms.FileInput()

        next_url = request.POST.get('next') or next_url
        next_url = next_url or request.GET.get('next', '/')
        self.fields['next'].initial = next_url

        self.is_creation = not self.instance.pk

        if self.is_creation:
            self.form_url = reverse('add_attachment', kwargs={
                'app_label': self._object._meta.app_label,
                'model_name': self._object._meta.model_name,
                'pk': self._object.pk
            })
        else:
            # When editing an attachment, changing its title won't rename!
            self.fields['title'].widget.attrs['readonly'] = True
            self.form_url = reverse('update_attachment', kwargs={
                'attachment_pk': self.instance.pk
            })

    def clean(self):
        cleaned_data = super().clean()
        if settings.PAPERCLIP_ENABLE_VIDEO or settings.PAPERCLIP_ENABLE_LINK:
            if cleaned_data['embed'] == 'Youtube' or cleaned_data['embed'] == 'Link':
                cleaned_data['attachment_file'] = ''
            else:
                cleaned_data['attachment_video'] = ''
                cleaned_data['attachment_link'] = ''
        return cleaned_data

    def success_url(self):
        return self.cleaned_data.get('next')

    def save(self, request, *args, **kwargs):
        obj = self._object
        self.instance.creator = request.user
        self.instance.content_object = obj
        return super().save(*args, **kwargs)
