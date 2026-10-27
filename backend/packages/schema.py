from __future__ import unicode_literals
import django_filters
import graphene
from django import forms
from django.db.models import Q
from graphene_django.debug import DjangoDebug
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoObjectType, DjangoListObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

from packages.models import TypeHemocomponent, TypeDiscard, Package


class TypeHemocomponentType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = TypeHemocomponent
        exclude_fields = ('created_at')


class TypeHemocomponentListType(DjangoListObjectType):
    class Meta:
        model = TypeHemocomponent
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class TypeHemocomponentFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)
    show_in_billing = django_filters.BooleanFilter(field_name='show_in_billing')
    show_in_fragmentation = django_filters.BooleanFilter(field_name='show_in_fragmentation')
    show_in_request_release = django_filters.BooleanFilter(field_name='show_in_request_release')

    class Meta:
        model = Package
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(TypeHemocomponentFilter, self).qs
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


class TypeDiscardType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = TypeDiscard
        exclude_fields = ('created_at')


class TypeDiscardListType(DjangoListObjectType):
    class Meta:
        model = TypeDiscard
        exclude_fields = ('created_at')
        filter_fields = {
            'name': ['icontains']
        }
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class TypeDiscardFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Package
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(TypeDiscardFilter, self).qs
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


class PackageType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = Package


class PackageListType(DjangoListObjectType):
    class Meta:
        model = Package
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class PackageFilter(django_filters.FilterSet):
    typepatient_id = django_filters.NumberFilter()
    typehemocomponent__show_in_billing = django_filters.BooleanFilter()
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Package
        fields = ['id', 'code', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(PackageFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(code__icontains=search_term) |
                        Q(typehemocomponent__name__icontains=search_term) |
                        Q(typepatient__name__contains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class Query(graphene.ObjectType):
    typehemocomponents = DjangoListObjectField(TypeHemocomponentListType, filterset_class=TypeHemocomponentFilter)
    typehemocomponent = DjangoObjectField(TypeHemocomponentType)

    typediscards = DjangoListObjectField(TypeDiscardListType, filterset_class=TypeDiscardFilter)
    typediscard = DjangoObjectField(TypeDiscardType)

    packages = DjangoListObjectField(PackageListType, filterset_class=PackageFilter)
    package = DjangoObjectField(PackageType)
