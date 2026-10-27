from __future__ import unicode_literals

import django_filters
import graphene
from django import forms
from django.db.models import Q
from graphene_django.debug import DjangoDebug
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoObjectType, DjangoListObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination
from sieves.models import ClinicalHistoryAnswer, ClinicalHistoryQuestion
from graphene.types import generic


class ClinicalHistoryQuestionFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = ClinicalHistoryQuestion
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(ClinicalHistoryQuestionFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                    Q(title__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class ClinicalHistoryQuestionType(DjangoObjectType):
    id = graphene.Int(source='pk')
    questions = generic.GenericScalar()

    class Meta:
        model = ClinicalHistoryQuestion
        exclude_fields = ('created_at')


class ClinicalHistoryQuestionListType(DjangoListObjectType):
    class Meta:
        model = ClinicalHistoryQuestion
        exclude_fields = ('created')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class ClinicalHistoryAnswerFilter(django_filters.FilterSet):
    register_at = django_filters.DateFilter()
    register_at__gte = django_filters.DateFilter(field_name='register_at', lookup_expr='gte')
    register_at__lte = django_filters.DateFilter(field_name='register_at', lookup_expr='lte')

    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = ClinicalHistoryAnswer
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(ClinicalHistoryAnswerFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(donation__donor__ci__icontains=search_term) |
                        Q(donation__donor__code__icontains=search_term) |
                        Q(donation__donor__first_name__icontains=search_term) |
                        Q(donation__donor__middle_name__icontains=search_term) |
                        Q(donation__donor__last_name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            ordering_terms = ordering.replace(' ', '').split(',')
            parent = parent.order_by(*ordering_terms)
        return parent


class ClinicalHistoryAnswerType(DjangoObjectType):
    id = graphene.Int(source='pk')
    responses = generic.GenericScalar()

    class Meta:
        model = ClinicalHistoryAnswer
        exclude_fields = ('created_at')


class ClinicalHistoryAnswerListType(DjangoListObjectType):
    class Meta:
        model = ClinicalHistoryAnswer
        exclude_fields = ('created')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class Query(graphene.ObjectType):
    clinicalhistoryanswer = DjangoObjectField(ClinicalHistoryAnswerType)
    clinicalhistoryanswers = DjangoListObjectField(ClinicalHistoryAnswerListType,
                                                   filterset_class=ClinicalHistoryAnswerFilter)

    clinicalhistoryquestion = DjangoObjectField(ClinicalHistoryQuestionType)
    clinicalhistoryquestions = DjangoListObjectField(ClinicalHistoryQuestionListType,
                                                     filterset_class=ClinicalHistoryQuestionFilter)
