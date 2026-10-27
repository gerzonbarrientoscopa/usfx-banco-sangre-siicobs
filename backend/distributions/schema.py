from __future__ import unicode_literals

import django_filters
import graphene
from django import forms
from django.db.models import Q
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoObjectType, DjangoListObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

from distributions.models import Distribution, DistributionItemFragmentation, DistributionItemFragmentationRefunded
from siicobs_main.services import BigInt


class DistributionFilter(django_filters.FilterSet):
    institution_id = django_filters.NumberFilter()
    type_payment = django_filters.CharFilter()
    employee_id = django_filters.NumberFilter()
    institution__type = django_filters.CharFilter()
    institution__type_payment = django_filters.CharFilter()
    register_at__gte = django_filters.DateFilter(field_name='register_at__date', lookup_expr='gte')
    register_at__lte = django_filters.DateFilter(field_name='register_at__date', lookup_expr='lte')
    age_patient = django_filters.NumberFilter()
    age_patient_type = django_filters.CharFilter()
    age_patient__gte = django_filters.NumberFilter(field_name='age_patient', lookup_expr='gte')
    age_patient__lte = django_filters.NumberFilter(field_name='age_patient', lookup_expr='lte')
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Distribution
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(DistributionFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(uuid__icontains=search_term) |
                        Q(patient__ci__icontains=search_term) |
                        Q(patient__first_name__icontains=search_term) |
                        Q(patient__middle_name__icontains=search_term) |
                        Q(patient__last_name__icontains=search_term) |
                        Q(medical__first_name__icontains=search_term) |
                        Q(medical__middle_name__icontains=search_term) |
                        Q(medical__last_name__icontains=search_term) |
                        Q(institution__name__icontains=search_term)
                ), conditions.connector)
                if isinstance(search_term, int):
                    conditions.add((
                        Q(itemfragmentations__itemfragmentation__donor_code=search_term)
                    ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class DistributionType(DjangoObjectType):
    id = graphene.Int(source='pk')
    invoice_number = graphene.Field(BigInt)
    status = graphene.String()
    type_payment = graphene.String()
    total_itemfragmentations = graphene.Int()

    class Meta:
        model = Distribution
        exclude_fields = ('created_at')

    def resolve_total_itemfragmentations(self, info):
        items = DistributionItemFragmentation.objects.filter(distribution_id=self.id)
        return len(items)


class DistributionListType(DjangoListObjectType):
    class Meta:
        model = Distribution
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class DistributionItemFragmentationFilter(django_filters.FilterSet):
    distribution__id = django_filters.NumberFilter()
    type_payment = django_filters.CharFilter(field_name='distribution__type_payment')
    register_at__gte = django_filters.DateFilter(field_name='distribution__register_at__date', lookup_expr='gte')
    register_at__lte = django_filters.DateFilter(field_name='distribution__register_at__date', lookup_expr='lte')
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = DistributionItemFragmentation
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(DistributionItemFragmentationFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(distribution__uuid__icontains=search_term) |
                        Q(itemfragmentation__donor_code__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class DistributionItemFragmentationType(DjangoObjectType):
    id = graphene.Int(source='pk')
    blood_group = graphene.String()

    class Meta:
        model = DistributionItemFragmentation
        exclude_fields = ('created_at')


class DistributionItemFragmentationRefundedType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = DistributionItemFragmentationRefunded
        exclude_fields = ('created_at')


class DistributionItemFragmentationListType(DjangoListObjectType):
    class Meta:
        model = DistributionItemFragmentation
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class Query(graphene.ObjectType):
    distributions = DjangoListObjectField(DistributionListType, filterset_class=DistributionFilter)
    distribution = DjangoObjectField(DistributionType)
    distribution_itemfragmentations = DjangoListObjectField(DistributionItemFragmentationListType,
                                                            filterset_class=DistributionItemFragmentationFilter)
    distribution_itemfragmentation = DjangoObjectField(DistributionItemFragmentationType)
