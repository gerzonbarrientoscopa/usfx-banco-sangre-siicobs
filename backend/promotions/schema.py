from __future__ import unicode_literals
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.db.models import Q
import django_filters
import graphene
from django import forms
from django.utils import timezone
from graphene.types import generic
from graphene_django.debug import DjangoDebug
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoObjectType, DjangoListObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

from donations.models import Donation
from donors.models import Donor
from promotions.models import Event


class EventType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = Event
        exclude_fields = ('created_at')


class EventFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Event
        fields = ['id', 'search', 'ordering', 'is_active']

    @property
    def qs(self):
        parent = super(EventFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(id__icontains=search_term) |
                        Q(name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class EventListType(DjangoListObjectType):
    class Meta:
        model = Event
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class Query(graphene.ObjectType):
    events = DjangoListObjectField(EventListType, filterset_class=EventFilter)
    event = DjangoObjectField(EventType)

    calendar_events = generic.GenericScalar(date=graphene.Argument(graphene.String),
                                            filter=graphene.Argument(graphene.String))

    def resolve_calendar_events(self, info, date, filter):
        if date != '':
            today_ = date.split('/')
            month = today_[1]
            year = today_[0]
        else:
            today = timezone.now()
            month = today.month
            year = today.year

        events = Event.objects.filter(init_at__year=year, init_at__month=month)
        newEvents = []
        color = 'purple'

        if filter == '1':
            for ev in events:
                if ev.is_active:
                    color = 'green'
                newEvents.append({
                    'id': ev.id,
                    'title': ev.name,
                    'start': ev.init_at.isoformat(),
                    'end': ev.end_at.isoformat(),
                    'color': color,
                    'is_active': ev.is_active
                })
        elif filter == '2':
            donors = Donor.objects.filter(birth_date__month=month, donations__event__isnull=False)

            for donor in donors:
                date_start = donor.birth_date.replace(year=int(year))
                color = 'blue'
                if donor.birth_date.month == timezone.now().month and donor.birth_date.day == timezone.now().day:
                    color = 'orange'
                newEvents.append({
                    'id': donor.id,
                    'title': '(%s) %s %s' % (donor.code, donor.middle_name, donor.first_name),
                    'start': date_start.isoformat(),
                    'end': date_start.isoformat(),
                    'color': color
                })
        elif filter == '3':
            donations = Donation.objects.filter(register_at__month=month, event__isnull=False)
            for donation in donations:
                if donation.donor.gender == 'M':
                    start_date = donation.register_at + relativedelta(months=3)
                else:
                    start_date = donation.register_at + relativedelta(months=4)

                datetime_object = datetime.strptime(str(start_date), '%Y-%m-%d')

                if datetime_object < datetime.now():
                    newEvents.append({
                        'id': donation.donor.id,
                        'title': '(%s) %s %s' % (
                            donation.donor.code, donation.donor.middle_name, donation.donor.first_name),
                        'start': start_date.isoformat(),
                        'end': start_date.isoformat(),
                        'color': 'black'
                    })
        return newEvents