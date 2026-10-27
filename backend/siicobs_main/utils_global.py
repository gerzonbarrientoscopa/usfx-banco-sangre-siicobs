# encoding:utf-8
import os

from dateutil import relativedelta
from django.conf import settings
from rest_framework import permissions
from datetime import date, datetime

from users.models import Employee


def link_callback(uri, rel):
    """ Convierte los URI HTML a las rutas absolutas del sistema para que xhtml2pdf pueda acceder a estos recursos"""
    # use short variable names
    sUrl = settings.STATIC_URL  # Typically /static/
    sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL  # Typically /static/media/
    mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


def is_technician(request):
    if request.user.is_superuser:
        return False
    else:
        return Employee.objects.filter(user=request.user, rol='TE').exists()


def is_supervisor(request):
    if request.user.is_superuser:
        return False
    else:
        return Employee.objects.filter(user=request.user, rol='SU').exists()


def is_administrator(request):
    if request.user.is_superuser:
        return False
    else:
        return Employee.objects.filter(user=request.user, rol='AD').exists()


def is_superadmin(request):
    return request.user.is_superuser


def get_age_from_birthday(born_day, today=date.today()):
    if born_day:
        return today.year - born_day.year - ((today.month, today.day) < (born_day.month, born_day.day))
    return 0


def get_string_age_from_birthday(born_day, today=date.today()):
    if born_day:
        born_datetime = datetime(born_day.year, born_day.month, born_day.day)
        today_datetime = datetime(today.year, today.month, today.day)
        delta = relativedelta.relativedelta(today_datetime, born_datetime)

        if delta.years > 0:
            return str(delta.years) + ' Y'
        elif delta.months > 0:
            return str(delta.months) + ' M'
        elif delta.days > 0:
            return str(delta.days) + ' D'
    return '0 Y'


class CustomObjectPermissions(permissions.DjangoObjectPermissions):
    """
    Similar to `DjangoObjectPermissions`, but adding 'view' permissions.
    """
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class SetCustomErrorMessagesMixin:
    '''
    Replaces built-in validator messages with messages, defined in Meta class.
    This mixin should be inherited before the actual Serializer class in order to call __init__ method.

    Example of Meta class:

    >>> class Meta:
    >>>     model = User
    >>>     fields = ('url', 'username', 'email', 'groups')
    >>>     custom_error_messages_for_validators = {
    >>>         'username': {
    >>>             UniqueValidator: _('This username is already taken. Please, try again'),
    >>>             RegexValidator: _('Invalid username')
    >>>         }
    >>>     }
    '''

    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        super(SetCustomErrorMessagesMixin, self).__init__(*args, **kwargs)
        self.replace_validators_messages()

    def replace_validators_messages(self):
        for field_name, validators_lookup in self.custom_error_messages_for_validators.items():
            # noinspection PyUnresolvedReferences
            for validator in self.fields[field_name].validators:
                if type(validator) in validators_lookup:
                    validator.message = validators_lookup[type(validator)]

    @property
    def custom_error_messages_for_validators(self):
        meta = getattr(self, 'Meta', None)
        return getattr(meta, 'custom_error_messages_for_validators', {})
