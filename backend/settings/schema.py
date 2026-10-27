from __future__ import unicode_literals

import django_filters
import graphene
from django import forms
from django.db.models import Q
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoObjectType, DjangoListObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination
from settings.models import Place, SettingPhisical, Reason


class PlaceFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Place
        fields = ['id', 'search', 'ordering']

    @property
    def qs(self):
        parent = super(PlaceFilter, self).qs
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


class PlaceType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = Place
        exclude_fields = ('created_at')


class PlaceListType(DjangoListObjectType):
    class Meta:
        model = Place
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class SettingPhysicalFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = SettingPhisical
        fields = ['id', 'search', 'ordering']

    @property
    def qs(self):
        parent = super(SettingPhysicalFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                    Q(place__name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class SettingPhysicalType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = SettingPhisical
        exclude_fields = ('created_at')


class SettingPhysicalListType(DjangoListObjectType):
    class Meta:
        model = SettingPhisical
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class ReasonFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Reason
        fields = ['id', 'search', 'ordering']

    @property
    def qs(self):
        parent = super(ReasonFilter, self).qs
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


class ReasonType(DjangoObjectType):
    id = graphene.Int(source='pk')
    type = graphene.String(source='type')

    class Meta:
        model = Reason
        exclude_fields = ('created')


class ReasonListType(DjangoListObjectType):
    class Meta:
        model = Reason
        exclude_fields = ('created')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class Query(graphene.ObjectType):
    places = DjangoListObjectField(PlaceListType, filterset_class=PlaceFilter)
    place = DjangoObjectField(PlaceType)

    settingphysicals = DjangoListObjectField(SettingPhysicalListType, filterset_class=SettingPhysicalFilter)
    settingphysical = DjangoObjectField(SettingPhysicalType)

    reasons = DjangoListObjectField(ReasonListType, filterset_class=ReasonFilter)
    reason = DjangoObjectField(ReasonType)
