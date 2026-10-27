from __future__ import unicode_literals
import django_filters
import graphene
from django import forms
from django.db.models import Q
from graphene_django.debug import DjangoDebug
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoObjectType, DjangoListObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

from donors.schema_donations import DonorType
from users.schema import PatientType
from provisions.models import Provision
from users.schema import EmployeeType


class ProvisionType(DjangoObjectType):
    id = graphene.Int(source='pk')
    donor = graphene.Field(DonorType)
    patient = graphene.Field(PatientType)
    employee = graphene.Field(EmployeeType)

    class Meta:
        model = Provision


class ProvisionListType(DjangoListObjectType):
    class Meta:
        model = Provision
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class ProvisionFilter(django_filters.FilterSet):
    patient_id = django_filters.NumberFilter()
    donor_id = django_filters.NumberFilter()
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Provision
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(ProvisionFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(donor__code__icontains=search_term) |
                        Q(donor__first_name__icontains=search_term) |
                        Q(donor__last_name__icontains=search_term) |
                        Q(donor__middle_name__icontains=search_term) |
                        Q(patient__first_name__icontains=search_term) |
                        Q(patient__last_name__icontains=search_term) |
                        Q(patient__middle_name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class Query(graphene.ObjectType):
    provisions = DjangoListObjectField(ProvisionListType, filterset_class=ProvisionFilter)
    provision = DjangoObjectField(ProvisionType)
