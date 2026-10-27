from __future__ import unicode_literals
import django_filters
import graphene
from django import forms
from django.db.models import Q
from graphene_django.debug import DjangoDebug
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoObjectType, DjangoListObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination
from donors.models import Donor, DonorHistory

FILTER_DONOR = {
    'donations': ['exact'],
    'first_name': ['icontains'],
    'middle_name': ['icontains'],
    'last_name': ['icontains'],
}


class DonorFilter(django_filters.FilterSet):
    donations__type_donation = django_filters.CharFilter(distinct=True)

    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Donor  # .objects.filter(donations__type_donation='VA')
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(DonorFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(ci__icontains=search_term) |
                        Q(code__icontains=search_term) |
                        Q(code_other__icontains=search_term) |
                        Q(first_name__icontains=search_term) |
                        Q(middle_name__icontains=search_term) |
                        Q(last_name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class DonorType(DjangoObjectType):
    id = graphene.Int(source='pk')
    group_abo = graphene.String()
    factor_rh = graphene.String()
    quantity_provision = graphene.Int()
    quantity_va_donation = graphene.Int()
    gender = graphene.String()
    country = graphene.String()
    is_available_for_new_donation = graphene.Boolean()
    last_effective_donation_at = graphene.Date()

    class Meta:
        model = Donor
        exclude_fields = ('created')
        # filter_fields = FILTER_DONOR


class DonorListType(DjangoListObjectType):
    class Meta:
        model = Donor
        exclude_fields = ('created')
        filter_fields = FILTER_DONOR
        pagination = LimitOffsetGraphqlPagination(default_limit=25)

class DonorHistoryType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = DonorHistory
        exclude_fields = ('created')
        # filter_fields = FILTER_DONOR


class Query(graphene.ObjectType):
    donors = DjangoListObjectField(DonorListType, filterset_class=DonorFilter)
    donor = DjangoObjectField(DonorType)

    next_donor_code = graphene.Int()

    def resolve_next_donor_code(self, info):
        top = Donor.objects.order_by('-code')[0]
        return top.code + 1

