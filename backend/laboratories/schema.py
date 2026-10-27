from __future__ import unicode_literals

import django_filters
import graphene
from django import forms
from django.db.models import Q
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoObjectType, DjangoListObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination
from graphene.types import generic

from fragmentations.models import ItemFragmentation
from fragmentations.schema import TypeIrregularAntiBodyType
from laboratories.models import Immunoserology, Immunohematology, SerologyProtocol
from laboratories.util_laboratories import get_results_serology


class ImmunohematologyFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)
    donation__type_donation = django_filters.CharFilter()
    register_at = django_filters.DateFilter()
    register_at__gte = django_filters.DateFilter(field_name='register_at', lookup_expr='gte')
    register_at__lte = django_filters.DateFilter(field_name='register_at', lookup_expr='lte')
    donation__rejected__isnull = django_filters.BooleanFilter(field_name='donation__rejected', lookup_expr='isnull')
    donation__rejected__reason__id = django_filters.NumberFilter(field_name='donation__rejected__reason__id')
    donation__rejected__reason__type = django_filters.CharFilter(field_name='donation__rejected__reason__type')
    donation__event__isnull = django_filters.BooleanFilter(field_name='donation__event', lookup_expr='isnull')
    donation__event__id = django_filters.NumberFilter()
    donation__donor__gender = django_filters.CharFilter()
    donation__donor__age = django_filters.NumberFilter()
    donation__donor__age__gte = django_filters.NumberFilter(field_name='donation__donor__age', lookup_expr='gte')
    donation__donor__age__lte = django_filters.NumberFilter(field_name='donation__donor__age', lookup_expr='lte')
    donation__donor__id = django_filters.NumberFilter()

    class Meta:
        model = Immunohematology
        fields = ['id', 'search', 'ordering']

    @property
    def qs(self):
        parent = super(ImmunohematologyFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                    Q(donation__donor__code__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class ImmunohematologyType(DjangoObjectType):
    id = graphene.Int(source='pk')
    direct_abo = graphene.String(source='direct_abo')
    inverse_abo = graphene.String(source='inverse_abo')
    phenotype = graphene.String(source='phenotype')
    antikell = graphene.String(source='antikell')
    factor_rh = graphene.String(source='factor_rh')
    fsi = graphene.String(source='fsi')
    alb = graphene.String(source='alb')
    liss = graphene.String(source='liss')
    coombs = graphene.String(source='coombs')
    p2fsi = graphene.String(source='p2fsi')
    p2alb = graphene.String(source='p2alb')
    p2liss = graphene.String(source='p2liss')
    p2coombs = graphene.String(source='p2coombs')
    p3fsi = graphene.String(source='p3fsi')
    p3alb = graphene.String(source='p3alb')
    p3liss = graphene.String(source='p3liss')
    p3coombs = graphene.String(source='p3coombs')
    type_irregular_antibody = graphene.Field(TypeIrregularAntiBodyType)
    exist_irregular_antibody = graphene.Boolean()

    class Meta:
        model = Immunohematology
        exclude_fields = ('created_at')

    def resolve_type_irregular_antibody(self, info):
        item = ItemFragmentation.objects.filter(
            fragmentation__extraction__donation__immunohematology__id=self.id).first()
        if item and item.type_irregular_antibody:
            return item.type_irregular_antibody
        return None

    def resolve_exist_irregular_antibody(self, info):
        return self.exists_irregular_antibodies


class ImmunohematologyListType(DjangoListObjectType):
    class Meta:
        model = Immunohematology
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class ImmunoserologyFilter(django_filters.FilterSet):
    donation__type_donation = django_filters.CharFilter()
    register_at = django_filters.DateFilter()
    register_at__gte = django_filters.DateFilter(field_name='register_at', lookup_expr='gte')
    register_at__lte = django_filters.DateFilter(field_name='register_at', lookup_expr='lte')
    donation__rejected__isnull = django_filters.BooleanFilter(field_name='donation__rejected', lookup_expr='isnull')
    donation__rejected__reason__id = django_filters.NumberFilter(field_name='donation__rejected__reason__id')
    donation__rejected__reason__type = django_filters.CharFilter(field_name='donation__rejected__reason__type')
    donation__event__isnull = django_filters.BooleanFilter(field_name='donation__event', lookup_expr='isnull')
    donation__event__id = django_filters.NumberFilter()
    donation__donor__gender = django_filters.CharFilter()
    donation__donor__age = django_filters.NumberFilter()
    donation__donor__age__gte = django_filters.NumberFilter(field_name='donation__donor__age', lookup_expr='gte')
    donation__donor__age__lte = django_filters.NumberFilter(field_name='donation__donor__age', lookup_expr='lte')
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Immunoserology
        fields = ['id', 'search', 'ordering']

    @property
    def qs(self):
        parent = super(ImmunoserologyFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                    Q(donation__donor__code__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class ImmunoserologyType(DjangoObjectType):
    id = graphene.Int(source='pk')
    is_reactive = graphene.Boolean()

    class Meta:
        model = Immunoserology
        exclude_fields = ('created_at')

    def resolve_is_reactive(self, info):
        return not get_results_serology(self)


class ImmunoserologyListType(DjangoListObjectType):
    class Meta:
        model = Immunoserology
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class SerologyProtocolFilter(django_filters.FilterSet):
    register_at = django_filters.DateFilter()
    register_at__gte = django_filters.DateFilter(field_name='register_at', lookup_expr='gte')
    register_at__lte = django_filters.DateFilter(field_name='register_at', lookup_expr='lte')
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = SerologyProtocol
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(SerologyProtocolFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                    Q(industry__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class SerologyProtocolType(DjangoObjectType):
    id = graphene.Int(source='pk')
    values = generic.GenericScalar()
    type = graphene.String()

    class Meta:
        model = SerologyProtocol
        exclude_fields = ('created_at')


class SerologyProtocolListType(DjangoListObjectType):
    class Meta:
        model = SerologyProtocol
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class Query(graphene.ObjectType):
    immunoserologies = DjangoListObjectField(ImmunoserologyListType, filterset_class=ImmunoserologyFilter)
    immunoserology = DjangoObjectField(ImmunoserologyType)

    serologyprotocols = DjangoListObjectField(SerologyProtocolListType, filterset_class=SerologyProtocolFilter)
    serologyprotocol = DjangoObjectField(SerologyProtocolType)

    immunohematologies = DjangoListObjectField(ImmunohematologyListType, filterset_class=ImmunohematologyFilter)
    immunohematology = DjangoObjectField(ImmunohematologyType)
