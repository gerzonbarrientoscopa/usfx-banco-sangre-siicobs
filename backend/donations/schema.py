from __future__ import unicode_literals
import django_filters
import graphene
from django import forms
from django.db.models import Q, Sum
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoObjectType, DjangoListObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination
from donations.models import Donation, PhysicalAnalysis, Exam, Rejected
from graphene.types import generic


class DonationFilter(django_filters.FilterSet):
    type_donation = django_filters.CharFilter()
    type_process = django_filters.CharFilter()
    register_at = django_filters.DateFilter()
    register_at__gte = django_filters.DateFilter(field_name='register_at', lookup_expr='gte')
    register_at__lte = django_filters.DateFilter(field_name='register_at', lookup_expr='lte')
    rejected__isnull = django_filters.BooleanFilter(field_name='rejected', lookup_expr='isnull')
    rejected__reason__type = django_filters.CharFilter(field_name='rejected__reason__type')
    rejected__reason_id = django_filters.CharFilter(field_name='rejected__reason_id')
    event__isnull = django_filters.BooleanFilter(field_name='event', lookup_expr='isnull')
    extraction__adversereaction__isnull = django_filters.BooleanFilter(field_name='extraction__adversereaction',
                                                                       lookup_expr='isnull')
    event__id = django_filters.NumberFilter()
    patient__id = django_filters.NumberFilter()
    donor__id = django_filters.NumberFilter()
    donor__code = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'd')], field_class=forms.CharField)
    donor__gender = django_filters.CharFilter()
    donor__age = django_filters.NumberFilter()
    donor__age__gte = django_filters.NumberFilter(field_name='donor__age', lookup_expr='gte')
    donor__age__lte = django_filters.NumberFilter(field_name='donor__age', lookup_expr='lte')
    donor__can_donate = django_filters.BooleanFilter(field_name='donor__can_donate')
    clinicalhistoryanswer__isnull = django_filters.BooleanFilter(field_name='clinicalhistoryanswer',
                                                                 lookup_expr='isnull')
    physicalanalysis__isnull = django_filters.BooleanFilter(field_name='physicalanalysis', lookup_expr='isnull')
    extraction__isnull = django_filters.BooleanFilter(field_name='extraction', lookup_expr='isnull')
    immunohematology__isnull = django_filters.BooleanFilter(field_name='immunohematology', lookup_expr='isnull')
    immunoserology__isnull = django_filters.BooleanFilter(field_name='immunoserology', lookup_expr='isnull')
    exam__isnull = django_filters.BooleanFilter(field_name='exam', lookup_expr='isnull')
    extraction__selfexclusion__isnull = django_filters.BooleanFilter(field_name='extraction__selfexclusion',
                                                                     lookup_expr='isnull')
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Donation
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(DonationFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(donor__ci__icontains=search_term) |
                        Q(donor__code__icontains=search_term) |
                        Q(donor__code_other__icontains=search_term) |
                        Q(donor__first_name__icontains=search_term) |
                        Q(donor__last_name__icontains=search_term) |
                        Q(donor__middle_name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            ordering_terms = ordering.replace(' ', '').split(',')
            parent = parent.order_by(*ordering_terms)
        return parent


class DonationType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = Donation
        exclude_fields = ('created')


class DonationListType(DjangoListObjectType):
    class Meta:
        model = Donation
        exclude_fields = ('created')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class ExamFilter(django_filters.FilterSet):
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
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Exam
        fields = ['id', 'search', 'ordering']

    @property
    def qs(self):
        parent = super(ExamFilter, self).qs
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
                        Q(donation__donor__last_name__icontains=search_term) |
                        Q(donation__donor__middle_name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class ExamType(DjangoObjectType):
    id = graphene.Int(source='pk')
    blood_group = graphene.String(source='blood_group')
    chagas = graphene.String(source='chagas')
    rpr = graphene.String(source='rpr')
    history = generic.GenericScalar(source='history')

    class Meta:
        model = Exam
        exclude_fields = 'created_at'
        filter_fields = {
            'donation': ['exact']
        }


class ExamListType(DjangoListObjectType):
    class Meta:
        model = Exam
        exclude_fields = ('created')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class RejectedFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Rejected
        fields = ['id', 'search', 'ordering']

    @property
    def qs(self):
        parent = super(RejectedFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(donation__donor__code__icontains=search_term) |
                        Q(donation__donor__first_name__icontains=search_term) |
                        Q(donation__donor__middle_name__icontains=search_term) |
                        Q(donation__donor__last_name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class RejectedType(DjangoObjectType):
    id = graphene.Int(source='pk')
    resource = graphene.String(source='resource')

    class Meta:
        model = Rejected
        exclude_fields = ('created_at')


class RejectedListType(DjangoListObjectType):
    class Meta:
        model = Rejected
        exclude_fields = ('created')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class PhysicalAnalysisFilter(django_filters.FilterSet):
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
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = PhysicalAnalysis
        fields = ['id', 'search', 'ordering']

    @property
    def qs(self):
        parent = super(PhysicalAnalysisFilter, self).qs
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
                        Q(donation__donor__last_name__icontains=search_term) |
                        Q(donation__donor__middle_name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class PhysicalAnalysisType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = PhysicalAnalysis
        exclude_fields = ('created_at')


class PhysicalAnalysisListType(DjangoListObjectType):
    class Meta:
        model = PhysicalAnalysis
        exclude_fields = ('created')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class Query(graphene.ObjectType):
    donations = DjangoListObjectField(DonationListType, filterset_class=DonationFilter)
    donation = DjangoObjectField(DonationType)

    exams = DjangoListObjectField(ExamListType, filterset_class=ExamFilter)
    exam = DjangoObjectField(ExamType)

    rejecteds = DjangoListObjectField(RejectedListType, filterset_class=RejectedFilter)
    rejected = DjangoObjectField(RejectedType)

    physicalanalyses = DjangoListObjectField(PhysicalAnalysisListType, filterset_class=PhysicalAnalysisFilter)
    physicalanalysis = DjangoObjectField(PhysicalAnalysisType)
