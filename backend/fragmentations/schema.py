from __future__ import unicode_literals
import django_filters
import graphene
from django import forms
from django.db.models import Q
from graphene_django.debug import DjangoDebug
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoObjectType, DjangoListObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

from donors.models import Donor
from fragmentations.models import Fragmentation, ItemFragmentation, Discard, Release, ReleaseRequest, \
    ReleaseTypeHemocomponent, TypeIrregularAntiBody


class FragmentationFilter(django_filters.FilterSet):
    extraction__donation__type_donation = django_filters.CharFilter()
    register_at = django_filters.DateFilter()
    register_at__gte = django_filters.DateFilter(field_name='register_at', lookup_expr='gte')
    register_at__lte = django_filters.DateFilter(field_name='register_at', lookup_expr='lte')
    register_at__lt = django_filters.DateFilter(field_name='register_at', lookup_expr='lt')
    employee_id = django_filters.NumberFilter()
    extraction__donation__rejected__isnull = django_filters.BooleanFilter(field_name='extraction__donation__rejected',
                                                                          lookup_expr='isnull')
    extraction__donation__rejected__reason__id = django_filters.NumberFilter(
        field_name='extraction__donation__rejected__reason__id')
    extraction__donation__rejected__reason__type = django_filters.CharFilter(
        field_name='extraction__donation__rejected__reason__type')
    extraction__donation__event__isnull = django_filters.BooleanFilter(field_name='extraction__donation__event',
                                                                       lookup_expr='isnull')
    extraction__donation__event__id = django_filters.NumberFilter()
    extraction__donation__donor__gender = django_filters.CharFilter()
    extraction__donation__donor__age = django_filters.NumberFilter()
    extraction__donation__donor__age__gte = django_filters.NumberFilter(field_name='extraction__donation__donor__age',
                                                                        lookup_expr='gte')
    extraction__donation__donor__age__lte = django_filters.NumberFilter(field_name='extraction__donation__donor__age',
                                                                        lookup_expr='lte')
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Fragmentation
        fields = ['id', 'search', 'ordering', 'extraction__donation__id']

    @property
    def qs(self):
        parent = super(FragmentationFilter, self).qs
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


class FragmentationType(DjangoObjectType):
    id = graphene.Int(source='pk')
    donor_code = graphene.Int()
    total_itemfragmentations = graphene.Int()

    class Meta:
        model = Fragmentation
        exclude_fields = ('created_at')

    def resolve_donor_code(self, info):
        donor_code = Donor.objects.get(donations__extraction__fragmentation__id=self.id).code
        return donor_code

    def resolve_total_itemfragmentations(self, info):
        items = ItemFragmentation.objects.filter(fragmentation__id=self.id)
        return len(items)


class FragmentationListType(DjangoListObjectType):
    class Meta:
        model = Fragmentation
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class ItemFragmentationFilter(django_filters.FilterSet):
    fragmentation__id = django_filters.NumberFilter()
    register_at__gte = django_filters.DateFilter(field_name='fragmentation__extraction__donation__register_at',
                                                 lookup_expr='gte')
    register_at__lte = django_filters.DateFilter(field_name='fragmentation__extraction__donation__register_at',
                                                 lookup_expr='lte')
    item_register_at__gte = django_filters.DateFilter(field_name='register_at', lookup_expr='gte')
    item_register_at__lte = django_filters.DateFilter(field_name='register_at', lookup_expr='lte')
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)
    release__isnull = django_filters.BooleanFilter(field_name='release', lookup_expr='isnull')
    discard__isnull = django_filters.BooleanFilter(field_name='discard', lookup_expr='isnull')
    typehemocomponent_id = django_filters.NumberFilter(field_name='typehemocomponent_id', lookup_expr='exact')
    is_distributed = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                       field_class=forms.CharField)
    only_release_or_discard = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                       field_class=forms.CharField)

    # status__in = django_filters.MultipleChoiceFilter(field_name='status', lookup_expr='in')

    class Meta:
        model = ItemFragmentation
        # fields = ['id', 'search', 'ordering', 'release__isnull', 'status__in']
        fields = {'status': ['exact', 'in'], 'fragmentation__extraction__donation__id': ['exact'], 'id': ['exact']}

    @property
    def qs(self):
        parent = super(ItemFragmentationFilter, self).qs
        search = self.data.get('search', None)
        is_distributed = self.data.get('is_distributed', None)
        only_release_or_discard = self.data.get('only_release_or_discard', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(donor_code__icontains=search_term) |
                        Q(typehemocomponent__name__icontains=search_term) |
                        Q(typehemocomponent__acronym__icontains=search_term) |
                        Q(typediscard__name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if is_distributed == 'true':
            conditions = Q()
            conditions.add(
                (~Q(distributionitemfragmentations__distributionitemfragmentationrefunded__isnull=True) &
                 Q(distributionitemfragmentations__distributionitemfragmentationrefunded__isnull=False)
                 ), conditions.AND)
            conditions.add((
                Q(distributionitemfragmentations__isnull=True)
            ), conditions.OR)

            parent = parent.filter(conditions).distinct()

        if only_release_or_discard == 'true':
            conditions = Q()
            conditions.add(
                (Q(release__isnull=False) |
                 Q(discard__isnull=False)
                 ), conditions.OR)
            parent = parent.filter(conditions).distinct()

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class ItemFragmentationType(DjangoObjectType):
    id = graphene.Int(source='pk')
    status = graphene.String(source='status')

    class Meta:
        model = ItemFragmentation
        exclude_fields = ('created_at')


class ItemFragmentationListType(DjangoListObjectType):
    class Meta:
        model = ItemFragmentation
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class DiscardFilter(django_filters.FilterSet):
    typehemocomponent_id = django_filters.NumberFilter(field_name='itemfragmentation__typehemocomponent_id',
                                                       lookup_expr='exact')
    register_at__gte = django_filters.DateFilter(field_name='register_at', lookup_expr='gte')
    register_at__lte = django_filters.DateFilter(field_name='register_at', lookup_expr='lte')
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Discard
        fields = ['id', 'search', 'ordering']

    @property
    def qs(self):
        parent = super(DiscardFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(itemfragmentation__donor_code__icontains=search_term) |
                        Q(itemfragmentation__typehemocomponent__name__icontains=search_term) |
                        Q(itemfragmentation__typehemocomponent__acronym__icontains=search_term) |
                        Q(itemfragmentation__typediscard__name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class DiscardType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = Discard
        exclude_fields = ('created_at')


class DiscardListType(DjangoListObjectType):
    class Meta:
        model = Discard
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class ReleaseFilter(django_filters.FilterSet):
    typehemocomponent_id = django_filters.NumberFilter(field_name='itemfragmentation__typehemocomponent_id',
                                                       lookup_expr='exact')
    register_at__gte = django_filters.DateFilter(field_name='register_at', lookup_expr='gte')
    register_at__lte = django_filters.DateFilter(field_name='register_at', lookup_expr='lte')
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = Release
        fields = ['id', 'search', 'ordering']

    @property
    def qs(self):
        parent = super(ReleaseFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(itemfragmentation__donor_code__icontains=search_term) |
                        Q(itemfragmentation__typehemocomponent__name__icontains=search_term) |
                        Q(itemfragmentation__typehemocomponent__acronym__icontains=search_term) |
                        Q(itemfragmentation__typediscard__name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        conditions = Q()
        conditions.add(
            (~Q(itemfragmentation__distributionitemfragmentations__distributionitemfragmentationrefunded__isnull=True)
             & Q(itemfragmentation__distributionitemfragmentations__distributionitemfragmentationrefunded__isnull=False)
             ), conditions.AND)
        conditions.add((
            Q(itemfragmentation__distributionitemfragmentations__isnull=True)
        ), conditions.OR)

        parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class ReleaseType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = Release
        exclude_fields = ('created_at')


class ReleaseListType(DjangoListObjectType):
    class Meta:
        model = Release
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class ReleaseRequestFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = ReleaseRequest
        fields = ['id', 'search', 'ordering']

    @property
    def qs(self):
        parent = super(ReleaseRequestFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(description__icontains=search_term) |
                        Q(attendant__first_name__icontains=search_term) |
                        Q(attendant__last_name__icontains=search_term) |
                        Q(attendant__middle_name__icontains=search_term) |
                        Q(medical__first_name__icontains=search_term) |
                        Q(medical__last_name__icontains=search_term) |
                        Q(medical__middle_name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class ReleaseRequestType(DjangoObjectType):
    id = graphene.Int(source='pk')
    status = graphene.Int(source='status')

    class Meta:
        model = ReleaseRequest
        exclude_fields = ('created_at')


class ReleaseTypeHemocomponentType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = ReleaseTypeHemocomponent
        exclude_fields = ('created_at')


class ReleaseRequestListType(DjangoListObjectType):
    class Meta:
        model = ReleaseRequest
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class TypeIrregularAntiBodyFilter(django_filters.FilterSet):
    search = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                               field_class=forms.CharField)
    ordering = django_filters.LookupChoiceFilter(lookup_choices=[('icontains', 'This is a description')],
                                                 field_class=forms.CharField)

    class Meta:
        model = TypeIrregularAntiBody
        fields = ['id', 'search', 'ordering']

    @property
    def qs(self):
        parent = super(TypeIrregularAntiBodyFilter, self).qs
        search = self.data.get('search', None)
        ordering = self.data.get('ordering', None)
        search_terms = None

        if search is not None:
            search_terms = search.replace(',', ' ').split()

        if search_terms:
            conditions = Q()
            for search_term in search_terms:
                conditions.add((
                        Q(recommendation__icontains=search_term) |
                        Q(name__icontains=search_term)
                ), conditions.connector)
            parent = parent.filter(conditions)

        if ordering is not None:
            sort = ordering.split(',')
            parent = parent.order_by(*sort)
        return parent


class TypeIrregularAntiBodyType(DjangoObjectType):
    id = graphene.Int(source='pk')

    class Meta:
        model = TypeIrregularAntiBody
        exclude_fields = ('created_at')


class TypeIrregularAntiBodyListType(DjangoListObjectType):
    class Meta:
        model = TypeIrregularAntiBody
        exclude_fields = ('created_at')
        pagination = LimitOffsetGraphqlPagination(default_limit=25)


class Query(graphene.ObjectType):
    fragmentations = DjangoListObjectField(FragmentationListType, filterset_class=FragmentationFilter)
    fragmentation = DjangoObjectField(FragmentationType)

    itemfragmentations = DjangoListObjectField(ItemFragmentationListType, filterset_class=ItemFragmentationFilter)
    itemfragmentation = DjangoObjectField(ItemFragmentationType)

    discards = DjangoListObjectField(DiscardListType, filterset_class=DiscardFilter)
    discard = DjangoObjectField(DiscardType)

    releases = DjangoListObjectField(ReleaseListType, filterset_class=ReleaseFilter)
    release = DjangoObjectField(ReleaseType)

    releaserequests = DjangoListObjectField(ReleaseRequestListType, filterset_class=ReleaseRequestFilter)
    releaserequest = DjangoObjectField(ReleaseRequestType)

    type_irregular_antibodies = DjangoListObjectField(TypeIrregularAntiBodyListType,
                                                      filterset_class=TypeIrregularAntiBodyFilter)
    type_irregular_antibody = DjangoObjectField(TypeIrregularAntiBodyType)
