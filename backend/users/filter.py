from __future__ import unicode_literals

import django_filters
from django import forms
from django.db.models import Q

from users.models import Employee, Institution, Medical
from django.contrib.auth.models import User, Group


class InstitutionFilter(django_filters.FilterSet):
    institution_billing_month = django_filters.NumberFilter(field_name='institutionbilling__month', exclude=True)
    # institution_billing_year = django_filters.NumberFilter(field_name='institutionbilling__year', exclude=True, lookup_expr='exact')

    distribution_month = django_filters.NumberFilter(field_name='distribution__register_at__month', distinct=True)
    distribution_year = django_filters.NumberFilter(field_name='distribution__register_at__year', distinct=True)
    distribution_type_payment = django_filters.NumberFilter(field_name='distribution__type_payment', distinct=True)
    has_distribution = django_filters.BooleanFilter(field_name='distribution', lookup_expr='isnull', exclude=True)

    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Institution
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(InstitutionFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(id__icontains=search_term) |
                        Q(name__icontains=search_term) |
                        Q(department__icontains=search_term) |
                        Q(nit__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class EmployeeFilter(django_filters.FilterSet):
    user__username = django_filters.CharFilter()
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Employee
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(EmployeeFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(id__icontains=search_term) |
                        Q(ci__icontains=search_term) |
                        Q(first_name__icontains=search_term) |
                        Q(middle_name__icontains=search_term) |
                        Q(last_name__icontains=search_term) |
                        Q(institution__name__icontains=search_term) |
                        Q(user__username__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class MedicalFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Medical
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(MedicalFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(id__icontains=search_term) |
                        Q(first_name__icontains=search_term) |
                        Q(middle_name__icontains=search_term) |
                        Q(last_name__icontains=search_term) |
                        Q(institution__name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class GroupFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Group
        fields = ['id', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(GroupFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(id__icontains=search_term) |
                        Q(name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent
