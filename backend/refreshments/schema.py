from __future__ import unicode_literals

import django_filters
import graphene
from django import forms
from django.db.models import Q
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoObjectType, DjangoListObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

from refreshments.models import Menu, ExtractionRefreshment

class MenuFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Menu
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(MenuFilter, self).qs
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


class MenuType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = Menu
        exclude_fields = ('created_at')


class MenuListType(DjangoListObjectType):
    class Meta:
        model = Menu
        exclude_fields = ('created')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class ExtractionRefreshmentFilter(django_filters.FilterSet):
    register_at = django_filters.DateFilter()
    register_at__gte = django_filters.DateFilter(field_name='register_at', lookup_expr='gte')
    register_at__lte = django_filters.DateFilter(field_name='register_at', lookup_expr='lte')

    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = ExtractionRefreshment
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(ExtractionRefreshmentFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(extraction__donation__donor__code__icontains=search_term) |
                        Q(menu__name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class ExtractionRefreshmentType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = ExtractionRefreshment
        exclude_fields = ('created_at')


class ExtractionRefreshmentListType(DjangoListObjectType):
    class Meta:
        model = ExtractionRefreshment
        exclude_fields = ('created')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class Query(graphene.ObjectType):
    menus = DjangoListObjectField(MenuListType, filterset_class=MenuFilter)
    menu = DjangoObjectField(MenuType)

    extractionrefreshments = DjangoListObjectField(ExtractionRefreshmentListType,
                                                   filterset_class=ExtractionRefreshmentFilter)
    extractionrefreshment = DjangoObjectField(ExtractionRefreshmentType)
