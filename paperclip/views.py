from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.db.models.loading import get_model
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.template.context import RequestContext
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

from paperclip import app_settings
from .models import Attachment
from .forms import AttachmentForm
import json


def add_url_for_obj(obj):
    return reverse('add_attachment', kwargs={
                        'app_label': obj._meta.app_label,
                        'module_name': obj._meta.module_name,
                        'pk': obj.pk
                    })

@require_POST
@permission_required('paperclip.add_attachment', raise_exception=True)
def add_attachment(request, app_label, module_name, pk,
                   template_name='paperclip/add.html', extra_context={}):

    next_url = request.POST.get('next', '/')
    model = get_model(app_label, module_name)
    if model is None:
        return HttpResponseRedirect(next_url)
    obj = get_object_or_404(model, pk=pk)
    form = AttachmentForm(request, request.POST, request.FILES)

    if form.is_valid():
        attachment = form.save(request, obj)
        if app_settings['ACTION_HISTORY_ENABLED']:
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=attachment.content_type.id,
                object_id=obj.pk,
                object_repr=force_text(obj),
                action_flag=CHANGE,
                change_message=_('Add attachment %s') % attachment.title,
            )
        messages.success(request, _('Your attachment was uploaded.'))
        return HttpResponseRedirect(next_url)
    else:
        template_context = {
            'attachment_form': form,
            'attachment_form_url': add_url_for_obj(obj),
            'next': next_url,
        }
        template_context.update(extra_context)
        return render_to_response(template_name, template_context,
                                  RequestContext(request))


@permission_required('paperclip.delete_attachment', raise_exception=True)
def delete_attachment(request, attachment_pk):
    g = get_object_or_404(Attachment, pk=attachment_pk)
    can_delete = (request.user.has_perm('paperclip.delete_attachment_others') or
                  request.user == g.creator)
    if can_delete:
        g.delete()
        if app_settings['ACTION_HISTORY_ENABLED']:
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=g.content_type.id,
                object_id=g.object_id,
                object_repr=force_text(g.content_object),
                action_flag=CHANGE,
                change_message=_('Remove attachment %s') % g.title,
            )
        messages.success(request, _('Your attachment was deleted.'))
    else:
        messages.error(request, _('You are not allowed to delete this attachment.'))
    next_url = request.REQUEST.get('next', '/')
    return HttpResponseRedirect(next_url)


def ajax_validate_attachment(request):
    form = AttachmentForm(request, request.POST, request.FILES)
    return HttpResponse(json.dumps(form.errors), content_type='application/json')


@permission_required('paperclip.read_attachment', raise_exception=True)
def get_attachments(request, app_label, module_name, pk):

    try:
        ct = ContentType.objects.get_by_natural_key(app_label, module_name)
    except ContentType.DoesNotExist:
        raise Http404
    attachments = Attachment.objects.filter(content_type=ct, object_id=pk)
    reply = [
        {
            'id': attachment.id,
            'title': attachment.title,
            'legend': attachment.legend,
            'url': attachment.attachment_file.url,
            'type': attachment.filetype.type,
            'author': attachment.author,
            'filename': attachment.filename,
            'mimetype': attachment.mimetype,
            'is_image': attachment.is_image,
            'starred': attachment.starred,
        }
        for attachment in attachments
    ]
    return HttpResponse(json.dumps(reply), content_type='application/json')
