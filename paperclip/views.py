from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.db.models.loading import get_model
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext, Template
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

from paperclip import app_settings
from .models import Attachment
from .forms import AttachmentForm
import json


@require_POST
@permission_required('paperclip.add_attachment', raise_exception=True)
def add_attachment(request, app_label, model_name, pk,
                   attachment_form=AttachmentForm,
                   extra_context=None):
    model = get_model(app_label, model_name)
    obj = get_object_or_404(model, pk=pk)
    form = attachment_form(request, request.POST, request.FILES, object=obj)
    return _handle_attachment_form(request, obj, form,
                                   _('Add attachment %s'),
                                   _('Your attachment was uploaded.'),
                                   extra_context)


@require_http_methods(["GET", "POST"])
@permission_required('paperclip.change_attachment', raise_exception=True)
def update_attachment(request, attachment_pk,
                      attachment_form=AttachmentForm,
                      extra_context=None):
    attachment = get_object_or_404(Attachment, pk=attachment_pk)
    obj = attachment.content_object
    if request.method == 'POST':
        form = attachment_form(
            request, request.POST, request.FILES,
            instance=attachment,
            object=obj)
    else:
        form = attachment_form(
            request,
            instance=attachment,
            object=obj)
    return _handle_attachment_form(request, obj, form,
                                   _('Update attachment %s'),
                                   _('Your attachment was updated.'),
                                   extra_context)


def _handle_attachment_form(request, obj, form, change_msg, success_msg,
                            extra_context):
    if form.is_valid():
        attachment = form.save(request, obj)
        if app_settings['ACTION_HISTORY_ENABLED']:
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=attachment.content_type.id,
                object_id=obj.pk,
                object_repr=force_text(obj),
                action_flag=CHANGE,
                change_message=change_msg % attachment.title,
            )
        messages.success(request, success_msg)
        return HttpResponseRedirect(form.success_url())

    template_string = """{% load attachments_tags %}
        {% attachment_form object attachment_form %}"""

    context = RequestContext(request)
    context['object'] = obj
    context['attachment_form'] = form

    if extra_context is not None:
        context.update(extra_context)

    t = Template(template_string)

    return HttpResponse(t.render(context))


@permission_required('paperclip.delete_attachment', raise_exception=True)
def delete_attachment(request, attachment_pk):
    g = get_object_or_404(Attachment, pk=attachment_pk)
    can_delete = (
        request.user.has_perm('paperclip.delete_attachment_others') or
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
        error_msg = _('You are not allowed to delete this attachment.')
        messages.error(request, error_msg)
    next_url = request.GET.get('next', '/')
    return HttpResponseRedirect(next_url)


@permission_required('paperclip.change_attachment', raise_exception=True)
def star_attachment(request, attachment_pk):
    g = get_object_or_404(Attachment, pk=attachment_pk)
    g.starred = request.GET.get('unstar') is None
    g.save()
    if g.starred:
        change_message = _('Star attachment %s')
    else:
        change_message = _('Unstar attachment %s')
    if app_settings['ACTION_HISTORY_ENABLED']:
        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=g.content_type.id,
            object_id=g.object_id,
            object_repr=force_text(g.content_object),
            action_flag=CHANGE,
            change_message=change_message % g.title,
        )
    reply = {
        'status': 'ok',
        'starred': g.starred
    }
    return HttpResponse(json.dumps(reply), content_type='application/json')


@permission_required('paperclip.read_attachment', raise_exception=True)
def get_attachments(request, app_label, model_name, pk):

    try:
        ct = ContentType.objects.get_by_natural_key(app_label, model_name)
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
