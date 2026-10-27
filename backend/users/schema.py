from __future__ import unicode_literals

import django_filters
import graphene
from django.contrib.auth.models import User, Group, Permission
from django import forms
from django.db.models import Q
from graphene_django.debug import DjangoDebug
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoObjectType, DjangoListObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination
from siicobs_main.services import BigInt
from users.filter import InstitutionFilter, EmployeeFilter, MedicalFilter, GroupFilter

from users.models import Employee, Institution, Patient, Medical


class InstitutionType(DjangoObjectType):
    id = graphene.Int(source='pk')
    logo = graphene.String(source='logo')
    department = graphene.String()

    class Meta:
        model = Institution
        exclude_fields = ('created_at')


class InstitutionListType(DjangoListObjectType):
    class Meta:
        model = Institution
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class UserType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = User
        exclude_fields = ('created_at')


class GroupType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = Group
        exclude_fields = ('created_at')


class GroupListType(DjangoListObjectType):
    class Meta:
        model = Group
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class PermissionType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = Permission
        exclude_fields = ('created_at')


class EmployeeType(DjangoObjectType):
    id = graphene.Int(source='pk')
    ci = graphene.Field(BigInt)

    class Meta:
        model = Employee
        exclude_fields = ('created_at')


class EmployeeListType(DjangoListObjectType):
    class Meta:
        model = Employee
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class MedicalType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = Medical
        exclude_fields = ('created_at')


class MedicalListType(DjangoListObjectType):
    class Meta:
        model = Medical
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class PatientType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = Patient
        exclude_fields = ('created_at')


class PatientListType(DjangoListObjectType):
    class Meta:
        model = Patient
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class PatientFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'ordering', 'search']

    @property
    def qs(self):
        parent = super(PatientFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((Q(id__icontains=search_term) |
                                Q(first_name__icontains=search_term) |
                                Q(middle_name__icontains=search_term) |
                                Q(last_name__icontains=search_term)), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            ordering_terms = ordering.replace(' ', '').split(',')
            parent = parent.order_by(*ordering_terms)
        return parent


class Query(graphene.ObjectType):
    institutions = DjangoListObjectField(InstitutionListType, filterset_class=InstitutionFilter)
    institution = DjangoObjectField(InstitutionType)

    employees = DjangoListObjectField(EmployeeListType, filterset_class=EmployeeFilter)
    employee = DjangoObjectField(EmployeeType)

    medicals = DjangoListObjectField(MedicalListType, filterset_class=MedicalFilter)
    medical = DjangoObjectField(MedicalType)

    groups = DjangoListObjectField(GroupListType, filterset_class=GroupFilter)
    group = DjangoObjectField(GroupType)

    patients = DjangoListObjectField(PatientListType, filterset_class=PatientFilter)
    patient = DjangoObjectField(PatientType)
