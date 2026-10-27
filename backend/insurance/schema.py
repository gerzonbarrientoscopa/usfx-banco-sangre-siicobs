from __future__ import unicode_literals
import django_filters
import graphene
from django import forms
from django.db.models import Q
from graphene_django.debug import DjangoDebug
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoObjectType, DjangoListObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

from packages.models import TypePatient


class TypePatientType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = TypePatient
        exclude_fields = ('created_at')


class TypePatientListType(DjangoListObjectType):
    class Meta:
        model = TypePatient
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class TypePatientFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = TypePatient
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(TypePatientFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                    Q(name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class Query(graphene.ObjectType):
    typepatients = DjangoListObjectField(TypePatientListType, filterset_class=TypePatientFilter)
    typepatient = DjangoObjectField(TypePatientType)
