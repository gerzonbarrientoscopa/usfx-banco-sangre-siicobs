from __future__ import unicode_literals

import json

import graphene
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from graphene.types import generic
from graphql_jwt.decorators import permission_required

from fragmentations.models import Release, Discard, Fragmentation, ItemFragmentation, ReleaseRequest, \
    ReleaseTypeHemocomponent
from fragmentations.schema import FragmentationType, DiscardType, ReleaseType, ReleaseRequestType
from packages.models import TypeHemocomponent
from users.models import Employee


def release_is_blocked_by_irregular_antibodies(itemfragmentation):
    if not itemfragmentation.typehemocomponent.blocks_release_with_irregular_antibodies:
        return False

    extraction = itemfragmentation.fragmentation.extraction
    if extraction is None:
        return False
    donation = extraction.donation
    try:
        immunohematology = donation.immunohematology
    except ObjectDoesNotExist:
        return False

    return immunohematology.exists_irregular_antibodies


def validate_release_items(items):
    blocked_items = [item for item in items if release_is_blocked_by_irregular_antibodies(item)]
    if blocked_items:
        hemocomponents = ', '.join(
            '{} ({})'.format(item.typehemocomponent.name, item.donor_code)
            for item in blocked_items
        )
        raise ValueError(
            'No se puede liberar: hay anticuerpos irregulares positivos para '
            'los siguientes hemocomponentes: {}.'.format(hemocomponents)
        )


class MassiveReleaseItemInput(graphene.InputObjectType):
    id = graphene.Int(required=True)


class CreateMassiveRelease(graphene.Mutation):
    release = graphene.Field(lambda: ReleaseType)

    class Arguments:
        hemocomponents = graphene.List(MassiveReleaseItemInput)
        employee_id = graphene.Int(required=True)
        register_id = graphene.Int(required=True)
        register_at = graphene.Date(required=True)
        observations = graphene.String()

    @permission_required(['fragmentations.add_release'])
    def mutate(self, info, hemocomponents, employee_id, register_id, register_at, **kwargs):
        employee = Employee.objects.filter(id=employee_id)
        if not employee:
            raise ValueError("Employee not exists.")

        if len(hemocomponents) == 0:
            raise ValueError("Not exist Hemocomponents")

        item_ids = [item.id for item in hemocomponents]
        items = list(
            ItemFragmentation.objects.filter(id__in=item_ids).select_related(
                'typehemocomponent',
                'fragmentation__extraction__donation__immunohematology'
            )
        )
        if len(items) != len(set(item_ids)):
            raise ValueError('No se encontraron todos los hemocomponentes seleccionados.')
        validate_release_items(items)

        release = Release()
        with transaction.atomic():
            for item in hemocomponents:
                release = Release(itemfragmentation_id=item.id, employee_id=employee_id, register_at=register_at,
                                  register_id=register_id)

                if kwargs.get('observations', None) is not None:
                    release.observations = kwargs.get('observations')

                release.save()

        return CreateMassiveRelease(release=release)


class MassiveDiscardItemInput(graphene.InputObjectType):
    id = graphene.Int(required=True)


class CreateMassiveDiscard(graphene.Mutation):
    discard = graphene.Field(lambda: DiscardType)

    class Arguments:
        hemocomponents = graphene.List(MassiveDiscardItemInput)
        employee_id = graphene.Int(required=True)
        register_id = graphene.Int(required=True)
        register_at = graphene.Date(required=True)
        reason = graphene.String(required=True)
        observations = graphene.String()

    @permission_required(['fragmentations.add_release'])
    def mutate(self, info, hemocomponents, employee_id, register_id, register_at, reason, **kwargs):
        employee = Employee.objects.filter(id=employee_id)
        if not employee:
            raise ValueError("Employee not exists.")

        if len(hemocomponents) == 0:
            raise ValueError("Not exist Hemocomponents")

        discard = Discard()
        for item in hemocomponents:
            discard = Discard(itemfragmentation_id=item.id, employee_id=employee_id, register_at=register_at,
                              register_id=register_id, reason=reason)

            if kwargs.get('observations', None) is not None:
                discard.observations = kwargs.get('observations')

            discard.save()

        return CreateMassiveDiscard(discard=discard)


class CreateFragmentation(graphene.Mutation):
    fragmentation = graphene.Field(lambda: FragmentationType)

    class Arguments:
        extraction_id = graphene.Int()
        quality_bag = graphene.String(required=True)
        total_hc = graphene.Float(required=True)
        employee_id = graphene.Int(required=True)
        register_id = graphene.Int(required=True)
        register_at = graphene.DateTime(required=True)
        observations = graphene.String()
        itemfragmentations = generic.GenericScalar()
        donor_code = graphene.Int(required=True)

    @permission_required(['fragmentations.add_fragmentation'])
    def mutate(self, info, donor_code, quality_bag, register_at, total_hc, register_id, employee_id, **kwargs):
        fragmentation = Fragmentation(quality_bag=quality_bag, total_hc=total_hc, register_at=register_at,
                                      register_id=register_id, employee_id=employee_id)

        if kwargs.get('extraction_id', None) is not None:
            fragmentation.extraction_id = kwargs.get('extraction_id')

        if kwargs.get('observations', None) is not None:
            fragmentation.observations = kwargs.get('observations')

        fragmentation.save()

        itemfragmentations = kwargs.get('itemfragmentations')
        for bp in itemfragmentations:
            type_h = TypeHemocomponent.objects.get(pk=bp.get('typehemocomponent_id'))
            object = ItemFragmentation(donor_code=donor_code,
                                       fragmentation_id=fragmentation.id,
                                       typehemocomponent=type_h, weight=bp['weight'],
                                       expiration_date=bp['expiration_date'],
                                       is_max_expiration_days=bp['is_max_expiration_days'],
                                       is_satellite_bag=bp['is_satellite_bag'],
                                       observations=bp['observations'])
            type_discard_id = bp.get('typediscard_id', None)
            if type_discard_id:
                object.typediscard_id = bp['typediscard_id']
            else:
                object.typediscard_id = None

            if bp.get('lot', None) is not None:
                object.lot = bp['lot']
            if bp.get('tubing') is not None:
                object.tubing = bp['tubing']

            object.save(force_insert=True)

        return CreateFragmentation(fragmentation=fragmentation)


class UpdateFragmentation(graphene.Mutation):
    fragmentation = graphene.Field(lambda: FragmentationType)

    class Arguments:
        id = graphene.Int(required=True)
        extraction_id = graphene.Int()
        quality_bag = graphene.String()
        total_hc = graphene.Float()
        employee_id = graphene.Int()
        register_id = graphene.Int()
        register_at = graphene.DateTime()
        observations = graphene.String()
        itemfragmentations = generic.GenericScalar()
        donor_code = graphene.Int(required=True)

    @permission_required(['fragmentations.change_fragmentation'])
    def mutate(self, info, id, donor_code, **kwargs):

        fragmentation = Fragmentation.objects.filter(id=id).first()
        old_total_hc = fragmentation.total_hc

        if fragmentation is None:
            raise ValueError('Fragmentation not found')

        if kwargs.get('extraction_id', None) is not None:
            fragmentation.extraction_id = kwargs.get('extraction_id')
        if kwargs.get('quality_bag', None) is not None:
            fragmentation.quality_bag = kwargs.get('quality_bag')
        if kwargs.get('total_hc', None) is not None:
            fragmentation.total_hc = kwargs.get('total_hc')
        if kwargs.get('employee_id', None) is not None:
            fragmentation.employee_id = kwargs.get('employee_id')
        if kwargs.get('register_id', None) is not None:
            fragmentation.register_id = kwargs.get('register_id')
        if kwargs.get('register_at', None) is not None:
            fragmentation.register_at = kwargs.get('register_at')
        if kwargs.get('observations', None) is not None:
            fragmentation.observations = kwargs.get('observations')

        fragmentation.save()

        itemfragmentations = kwargs.get('itemfragmentations')
        id_itemfragmentations = []
        for bp in itemfragmentations:
            typehecomponent = TypeHemocomponent.objects.get(pk=bp.get('typehemocomponent_id'))

            if bp.get('id'):
                itemfragmentation = ItemFragmentation.objects.get(id=bp['id'])
                itemfragmentation.donor_code = donor_code
                itemfragmentation.fragmentation_id = fragmentation.id
                itemfragmentation.typehemocomponent_id = bp['typehemocomponent_id']
                itemfragmentation.weight = bp['weight']
                itemfragmentation.expiration_date = bp['expiration_date']
                itemfragmentation.is_max_expiration_days = bp['is_max_expiration_days']
                itemfragmentation.is_satellite_bag = bp['is_satellite_bag']
                itemfragmentation.observations = bp['observations']

                type_discard_id = bp.get('typediscard_id', None)
                if type_discard_id:
                    itemfragmentation.typediscard_id = bp['typediscard_id']
                else:
                    itemfragmentation.typediscard_id = None

                if typehecomponent.can_add_bags:
                    if bp.get('lot', None) is not None:
                        itemfragmentation.lot = bp['lot']
                    if bp.get('tubing') is not None:
                        itemfragmentation.tubing = bp['tubing']
                else:
                    itemfragmentation.lot = None
                    itemfragmentation.tubing = None

                itemfragmentation.save()
                id_itemfragmentations.append(itemfragmentation.id)
            else:
                object = ItemFragmentation(donor_code=donor_code, fragmentation_id=fragmentation.id,
                                           typehemocomponent=typehecomponent, weight=bp['weight'],
                                           expiration_date=bp['expiration_date'],
                                           is_max_expiration_days = bp['is_max_expiration_days'],
                                           is_satellite_bag=bp['is_satellite_bag'],
                                           observations=bp['observations'])

                type_discard_id = bp.get('typediscard_id', None)
                if type_discard_id:
                    object.typediscard_id = bp['typediscard_id']
                else:
                    object.typediscard_id = None
                object.donor_code = donor_code

                if typehecomponent.can_add_bags:
                    if bp.get('lot', None) is not None:
                        object.lot = bp['lot']
                    if bp.get('tubing') is not None:
                        object.tubing = bp['tubing']
                else:
                    object.lot = None
                    object.tubing = None

                object.save()
                id_itemfragmentations.append(object.id)

        if len(itemfragmentations) < old_total_hc:
            ItemFragmentation.objects.filter(fragmentation_id=fragmentation.id).exclude(
                id__in=id_itemfragmentations).delete()

        return UpdateFragmentation(fragmentation=fragmentation)


class CreateDiscard(graphene.Mutation):
    discard = graphene.Field(lambda: DiscardType)

    class Arguments:
        itemfragmentation_id = graphene.Int(required=True)
        reason = graphene.String(required=True)
        employee_id = graphene.Int(required=True)
        register_id = graphene.Int(required=True)
        register_at = graphene.Date(required=True)
        observations = graphene.String()

    @permission_required(['fragmentations.add_discard'])
    def mutate(self, info, itemfragmentation_id, reason, employee_id, register_id, register_at, **kwargs):
        discard = Discard(itemfragmentation_id=itemfragmentation_id, reason=reason, register_at=register_at,
                          register_id=register_id, employee_id=employee_id)

        if kwargs.get('observations', None) is not None:
            discard.observations = kwargs.get('observations')

        discard.save()

        return CreateDiscard(discard=discard)


class UpdateDiscard(graphene.Mutation):
    discard = graphene.Field(lambda: DiscardType)

    class Arguments:
        id = graphene.Int(required=True)
        itemfragmentation_id = graphene.Int()
        reason = graphene.String()
        employee_id = graphene.Int()
        register_id = graphene.Int()
        register_at = graphene.Date()
        observations = graphene.String()

    @permission_required(['fragmentations.change_discard'])
    def mutate(self, info, id, **kwargs):

        discard = Discard.objects.filter(id=id).first()
        if discard is None:
            raise ValueError('Discard not found')

        if kwargs.get('itemfragmentation_id', None) is not None:
            discard.itemfragmentation_id = kwargs.get('itemfragmentation_id')
        if kwargs.get('employee_id', None) is not None:
            discard.employee_id = kwargs.get('employee_id')
        if kwargs.get('register_id', None) is not None:
            discard.register_id = kwargs.get('register_id')
        if kwargs.get('reason', None) is not None:
            discard.reason = kwargs.get('reason')
        if kwargs.get('register_at', None) is not None:
            discard.register_at = kwargs.get('register_at')
        if kwargs.get('observations', None) is not None:
            discard.observations = kwargs.get('observations')

        discard.save()

        return UpdateDiscard(discard=discard)


class DeleteDiscard(graphene.Mutation):
    discard = graphene.Field(lambda: DiscardType)

    class Arguments:
        id = graphene.Int(required=True)

    @permission_required(['fragmentations.delete_discard'])
    def mutate(self, info, id):
        discard = Discard.objects.filter(id=id).first()
        if discard is None:
            raise ValueError('Discard not found')

        discard.delete()

        return DeleteDiscard(discard=discard)


class CreateRelease(graphene.Mutation):
    release = graphene.Field(lambda: ReleaseType)

    class Arguments:
        itemfragmentation_id = graphene.Int(required=True)
        employee_id = graphene.Int(required=True)
        register_id = graphene.Int(required=True)
        register_at = graphene.Date(required=True)
        observations = graphene.String()

    @permission_required(['fragmentations.add_release'])
    def mutate(self, info, itemfragmentation_id, employee_id, register_id, register_at, **kwargs):
        itemfragmentation = ItemFragmentation.objects.select_related(
            'typehemocomponent',
            'fragmentation__extraction__donation__immunohematology'
        ).get(pk=itemfragmentation_id)
        validate_release_items([itemfragmentation])

        release = Release(itemfragmentation_id=itemfragmentation_id, register_at=register_at,
                          register_id=register_id, employee_id=employee_id)

        if kwargs.get('observations', None) is not None:
            release.observations = kwargs.get('observations')

        release.save()

        return CreateRelease(release=release)


class UpdateRelease(graphene.Mutation):
    release = graphene.Field(lambda: ReleaseType)

    class Arguments:
        id = graphene.Int(required=True)
        itemfragmentation_id = graphene.Int()
        employee_id = graphene.Int()
        register_id = graphene.Int()
        register_at = graphene.Date()
        observations = graphene.String()

    @permission_required(['fragmentations.change_release'])
    def mutate(self, info, id, **kwargs):

        release = Release.objects.filter(id=id).first()
        if release is None:
            raise ValueError('Release not found')

        if kwargs.get('itemfragmentation_id', None) is not None:
            itemfragmentation = ItemFragmentation.objects.select_related(
                'typehemocomponent',
                'fragmentation__extraction__donation__immunohematology'
            ).get(pk=kwargs.get('itemfragmentation_id'))
            validate_release_items([itemfragmentation])
            release.itemfragmentation_id = kwargs.get('itemfragmentation_id')
        if kwargs.get('employee_id', None) is not None:
            release.employee_id = kwargs.get('employee_id')
        if kwargs.get('register_id', None) is not None:
            release.register_id = kwargs.get('register_id')
        if kwargs.get('register_at', None) is not None:
            release.register_at = kwargs.get('register_at')
        if kwargs.get('observations', None) is not None:
            release.observations = kwargs.get('observations')

        release.save()

        return UpdateRelease(release=release)


class DeleteRelease(graphene.Mutation):
    release = graphene.Field(lambda: ReleaseType)

    class Arguments:
        id = graphene.Int(required=True)

    @permission_required(['fragmentations.delete_release'])
    def mutate(self, info, id):
        release = Release.objects.filter(id=id).first()
        if release is None:
            raise ValueError('Release not found')

        release.delete()

        return DeleteRelease(release=release)


class CreateReleaseRequest(graphene.Mutation):
    releaserequest = graphene.Field(lambda: ReleaseRequestType)

    class Arguments:
        register_at = graphene.DateTime(required=True)
        attendant_id = graphene.Int(required=True)
        employee_id = graphene.Int(required=True)
        medical_id = graphene.Int(required=True)
        status = graphene.String(required=True)
        description = graphene.String()
        typeHemocomponents = generic.GenericScalar()

    @permission_required(['fragmentations.add_releaserequest'])
    def mutate(self, info, register_at, attendant_id, employee_id, medical_id, status, **kwargs):
        releaserequest = ReleaseRequest(register_at=register_at, attendant_id=attendant_id, employee_id=employee_id,
                                        medical_id=medical_id, status=status)

        if kwargs.get('description', None) is not None:
            releaserequest.description = kwargs.get('description')

        releaserequest.save()

        type_hemocomponents = kwargs.get('typeHemocomponents')

        for bp in type_hemocomponents:
            type_h = TypeHemocomponent.objects.get(pk=bp.get('typehemocomponent')['id'])
            object = ReleaseTypeHemocomponent(release_id=releaserequest.id, typehemocomponent=type_h,
                                              quantity_release=bp['quantity_release'],
                                              quantity_request=bp['quantity_request'])
            object.save(force_insert=True)

        return CreateReleaseRequest(releaserequest=releaserequest)


class UpdateReleaseRequest(graphene.Mutation):
    releaserequest = graphene.Field(lambda: ReleaseRequestType)

    class Arguments:
        id = graphene.Int(required=True)
        register_at = graphene.DateTime()
        attendant_id = graphene.Int()
        employee_id = graphene.Int()
        medical_id = graphene.Int()
        status = graphene.String()
        description = graphene.String()
        typeHemocomponents = generic.GenericScalar()

    @permission_required(['fragmentation.change_releaserequest'])
    def mutate(self, info, id, **kwargs):

        releaserequest = ReleaseRequest.objects.filter(id=id).first()
        if releaserequest is None:
            raise ValueError('ReleaseRequest not found')

        if kwargs.get('register_at', None) is not None:
            releaserequest.register_at = kwargs.get('register_at')
        if kwargs.get('attendant_id', None) is not None:
            releaserequest.attendant_id = kwargs.get('attendant_id')
        if kwargs.get('employee_id', None) is not None:
            releaserequest.employee_id = kwargs.get('employee_id')
        if kwargs.get('medical_id', None) is not None:
            releaserequest.medical_id = kwargs.get('medical_id')
        if kwargs.get('status', None) is not None:
            releaserequest.status = kwargs.get('status')
        if kwargs.get('description', None) is not None:
            releaserequest.description = kwargs.get('description')

        releaserequest.save()

        ReleaseTypeHemocomponent.objects.filter(release__id=releaserequest.id).delete()

        type_hemocomponents = kwargs.get('typeHemocomponents')

        for bp in type_hemocomponents:
            typehecomponent = TypeHemocomponent.objects.get(pk=bp.get('typehemocomponent')['id'])
            object, created = ReleaseTypeHemocomponent.objects.get_or_create(release_id=releaserequest.id,
                                                                             typehemocomponent=typehecomponent,
                                                                             quantity_release=bp['quantity_release'],
                                                                             quantity_request=bp['quantity_request'])
            object.save()

        return UpdateReleaseRequest(releaserequest=releaserequest)


class Mutation(graphene.ObjectType):
    create_fragmentation = CreateFragmentation.Field()
    update_fragmentation = UpdateFragmentation.Field()

    create_discard = CreateDiscard.Field()
    update_discard = UpdateDiscard.Field()
    delete_discard = DeleteDiscard.Field()
    create_massive_discard = CreateMassiveDiscard.Field()

    create_release = CreateRelease.Field()
    update_release = UpdateRelease.Field()
    create_massive_release = CreateMassiveRelease.Field()
    delete_release = DeleteRelease.Field()

    create_releaserequest = CreateReleaseRequest.Field()
    update_releaserequest = UpdateReleaseRequest.Field()
