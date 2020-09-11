from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.admin.utils import construct_change_message
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str


def save_history(request, object, action, form, formset):
    if action is ADDITION:
        change_message = [{"added": {}}]
    elif action is DELETION:
        change_message = ""
    else:
        change_message = construct_change_message(form, formset, False)

    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=force_str(object),
        action_flag=action,
        change_message=change_message,
    )


def log_addition(request, object):
    save_history(
        request=request,
        object=object,
        action=ADDITION,
        form=None,
        formset=None,
    )


def log_change(request, object, form, formset):
    save_history(
        request=request,
        object=object,
        action=CHANGE,
        form=form,
        formset=formset,
    )


def log_deletion(request, object):
    save_history(
        request=request,
        object=object,
        action=DELETION,
        form=None,
        formset=None,
    )
