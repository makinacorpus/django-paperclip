from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from paperclip import app_settings
from .models import Attachment


class AttachmentForm(forms.ModelForm):

    if app_settings['ENABLE_VIDEO']:
        embed = forms.ChoiceField(
            label=_(u"Mode"),
            choices=((False, _('File')),
                     (True, _('Youtube/Soundcloud URL'))),
            widget=forms.RadioSelect(), initial=False)
    next = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Attachment
        if app_settings['ENABLE_VIDEO']:
            fields = ('embed', 'attachment_file', 'attachment_video',
                      'filetype', 'author', 'title', 'legend')
        else:
            fields = ('attachment_file', 'filetype', 'author', 'title',
                      'legend')

    def __init__(self, request, *args, **kwargs):
        self._object = kwargs.pop('object', None)
        next_url = kwargs.pop('next_url', None)

        super(AttachmentForm, self).__init__(*args, **kwargs)
        self.fields['legend'].widget.attrs['placeholder'] = _('Sunset on lake')
        self.fields['author'].initial = request.user

        # Allow to override filetype choices
        filetype_model = self.fields['filetype'].queryset.model
        self.fields['filetype'].queryset = filetype_model.objects_for(request)

        # Detect fields errors without uploading (using HTML5)
        self.fields['filetype'].widget.attrs['required'] = 'required'
        self.fields['author'].widget.attrs['pattern'] = '^\S.*'
        self.fields['legend'].widget.attrs['pattern'] = '^\S.*'

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
        cleaned_data = super(AttachmentForm, self).clean()
        if app_settings['ENABLE_VIDEO']:
            if cleaned_data['embed'] == 'True':
                cleaned_data['attachment_file'] = ''
            else:
                cleaned_data['attachment_video'] = ''
        return cleaned_data

    def success_url(self):
        return self.cleaned_data.get('next')

    def save(self, request, *args, **kwargs):
        obj = self._object
        self.instance.creator = request.user
        self.instance.content_type = ContentType.objects.get_for_model(obj)
        self.instance.object_id = obj.id
        return super(AttachmentForm, self).save(*args, **kwargs)
