from __future__ import unicode_literals

import django_filters
import graphene
from django import forms
from django.db.models import Q
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoObjectType, DjangoListObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

from extractions.models import Extraction, AdverseReaction, TypeAdverseReaction, SelfExclusion, TypeAnticoagulant


class TypeAnticoagulantFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = TypeAnticoagulant
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(TypeAnticoagulantFilter, self).qs
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


class TypeAnticoagulantType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = TypeAnticoagulant


class TypeAnticoagulantListType(DjangoListObjectType):
    class Meta:
        model = TypeAnticoagulant
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class ExtractionFilter(django_filters.FilterSet):
    donation__type_donation = django_filters.CharFilter()
    register_at = django_filters.DateFilter()
    register_at__gte = django_filters.DateFilter(field_name='register_at', lookup_expr='gte')
    register_at__lte = django_filters.DateFilter(field_name='register_at', lookup_expr='lte')
    donation__rejected__isnull = django_filters.BooleanFilter(field_name='donation__rejected', lookup_expr='isnull')
    donation__rejected__reason__type = django_filters.CharFilter(field_name='donation__rejected__reason__type')
    donation__event__isnull = django_filters.BooleanFilter(field_name='donation__event', lookup_expr='isnull')
    donation__event__id = django_filters.NumberFilter()

    donation__donor__gender = django_filters.CharFilter()
    donation__donor__age = django_filters.NumberFilter()
    donation__donor__age__gte = django_filters.NumberFilter(field_name='donation__donor__age', lookup_expr='gte')
    donation__donor__age__lte = django_filters.NumberFilter(field_name='donation__donor__age', lookup_expr='lte')

    adversereaction__isnull = django_filters.BooleanFilter(field_name='adversereaction', lookup_expr='isnull')
    selfexclusion__isnull = django_filters.BooleanFilter(field_name='selfexclusion', lookup_expr='isnull')
    fragmentation__isnull = django_filters.BooleanFilter(field_name='fragmentation', lookup_expr='isnull')
    immunohematology__isnull = django_filters.BooleanFilter(field_name='immunohematology', lookup_expr='isnull')
    immunoserology__isnull = django_filters.BooleanFilter(field_name='immunoserology', lookup_expr='isnull')
    apheresis__isnull = django_filters.BooleanFilter(field_name='apheresis', lookup_expr='isnull')
    extractionrefreshment__isnull = django_filters.BooleanFilter(field_name='extractionrefreshment',
                                                                 lookup_expr='isnull')

    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Extraction
        fields = ['id', 'donation__id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(ExtractionFilter, self).qs
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


class ExtractionType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = Extraction


class ExtractionListType(DjangoListObjectType):
    class Meta:
        model = Extraction
        exclude_fields = ('created')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class AdverseReactionFilter(django_filters.FilterSet):
    register_at = django_filters.DateFilter()
    register_at__gte = django_filters.DateFilter(field_name='register_at__date', lookup_expr='gte')
    register_at__lte = django_filters.DateFilter(field_name='register_at__date', lookup_expr='lte')

    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = AdverseReaction
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(AdverseReactionFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                    Q(extraction__donation__donor__code__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class AdverseReactionType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = AdverseReaction
        exclude_fields = ('created_at')


class AdverseReactionListType(DjangoListObjectType):
    class Meta:
        model = AdverseReaction
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class SelfExclusionFilter(django_filters.FilterSet):
    register_at = django_filters.DateFilter()
    register_at__gte = django_filters.DateFilter(field_name='register_at', lookup_expr='gte')
    register_at__lte = django_filters.DateFilter(field_name='register_at', lookup_expr='lte')

    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = SelfExclusion
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(SelfExclusionFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                    Q(extraction__donation__donor__code__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class SelfExclusionType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = SelfExclusion
        exclude_fields = ('created_at')


class SelfExclusionListType(DjangoListObjectType):
    class Meta:
        model = SelfExclusion
        exclude_fields = ('created')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class TypeAdverseReactionFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)
    show_in_conventional = django_filters.BooleanFilter()
    show_in_apheresis = django_filters.BooleanFilter()

    class Meta:
        model = TypeAdverseReaction
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(TypeAdverseReactionFilter, self).qs
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


class TypeAdverseReactionType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = TypeAdverseReaction
        exclude_fields = ('created_at')


class TypeAdverseReactionListType(DjangoListObjectType):
    class Meta:
        model = TypeAdverseReaction
        exclude_fields = ('created')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class Query(graphene.ObjectType):
    typeanticoagulants = DjangoListObjectField(TypeAnticoagulantListType, filterset_class=TypeAnticoagulantFilter)
    typeanticoagulante = DjangoObjectField(TypeAnticoagulantType)

    extractions = DjangoListObjectField(ExtractionListType, filterset_class=ExtractionFilter)
    extraction = DjangoObjectField(ExtractionType)

    adversereactions = DjangoListObjectField(AdverseReactionListType, filterset_class=AdverseReactionFilter)
    adversereaction = DjangoObjectField(AdverseReactionType)

    selfexclusions = DjangoListObjectField(SelfExclusionListType, filterset_class=SelfExclusionFilter)
    selfexclusion = DjangoObjectField(SelfExclusionType)

    typeadversereactions = DjangoListObjectField(TypeAdverseReactionListType, filterset_class=TypeAdverseReactionFilter)
    typeadversereaction = DjangoObjectField(TypeAdverseReactionType)
