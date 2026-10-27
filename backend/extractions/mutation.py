from __future__ import unicode_literals

from datetime import timedelta

import graphene
from graphene.types import generic
from graphql_jwt.decorators import permission_required

from extractions.models import Extraction, SelfExclusion, TypeAdverseReaction, AdverseReaction
from extractions.schema import ExtractionType, SelfExclusionType, TypeAdverseReactionType, AdverseReactionType


class CreateExtraction(graphene.Mutation):
    extraction = graphene.Field(lambda: ExtractionType)

    class Arguments:
        donation_id = graphene.Int(required=True)
        bags_quantity = graphene.Int(required=True)
        type_place = graphene.String(required=True)
        lot = graphene.String(required=True)
        tubing = graphene.String()
        barcode = graphene.String()
        weight = graphene.Float()
        arm = graphene.String()
        initial_time = graphene.Time(required=True)
        end_time = graphene.Time()
        total_time = graphene.Float()
        employee_id = graphene.Int(required=True)
        register_id = graphene.Int(required=True)
        observations = graphene.String()
        register_at = graphene.Date(required=True)
        typeanticoagulant_id = graphene.Int(required=True)

    @permission_required(['extractions.add_extraction'])
    def mutate(self, info, donation_id, type_place, bags_quantity, lot, initial_time, employee_id, register_id,
               register_at, typeanticoagulant_id, **kwargs):
        _extraction = Extraction.objects.filter(donation_id=donation_id).first()

        if _extraction is not None:
            raise ValueError('donation_id: debe ser unico')

        extraction = Extraction(donation_id=donation_id, type_place=type_place, bags_quantity=bags_quantity,
                                lot=lot, initial_time=initial_time, employee_id=employee_id,
                                register_id=register_id, typeanticoagulant_id=typeanticoagulant_id,
                                register_at=register_at)

        if kwargs.get('tubing', None) is not None:
            extraction.tubing = kwargs.get('tubing')
        if kwargs.get('arm', None) is not None:
            extraction.arm = kwargs.get('arm')
        if kwargs.get('barcode', None) is not None:
            extraction.barcode = kwargs.get('barcode')
        if kwargs.get('weight', None) is not None:
            extraction.weight = kwargs.get('weight')
        if kwargs.get('end_time', None) is not None:
            extraction.end_time = kwargs.get('end_time')
        if kwargs.get('total_time', None) is not None:
            extraction.total_time = kwargs.get('total_time')
        if kwargs.get('observations', None) is not None:
            extraction.observations = kwargs.get('observations')

        extraction.save()

        return CreateExtraction(extraction=extraction)


class UpdateExtraction(graphene.Mutation):
    extraction = graphene.Field(lambda: ExtractionType)

    class Arguments:
        id = graphene.Int(required=True)
        donation_id = graphene.Int()
        type_place = graphene.String()
        bags_quantity = graphene.Int()
        lot = graphene.String()
        tubing = graphene.String()
        barcode = graphene.String()
        weight = graphene.Float()
        arm = graphene.String()
        initial_time = graphene.Time()
        end_time = graphene.Time()
        total_time = graphene.Float()
        employee_id = graphene.Int()
        register_id = graphene.Int()
        observations = graphene.String()
        register_at = graphene.Date()

    @permission_required(['extractions.change_extraction'])
    def mutate(self, info, id, **kwargs):
        extraction = Extraction.objects.filter(id=id).first()
        if not extraction:
            raise ValueError("Extraction not exists.")

        if kwargs.get('donation_id', None) is not None:
            extraction.donation_id = kwargs.get('donation_id')
        if kwargs.get('bags_quantity', None) is not None:
            extraction.bags_quantity = kwargs.get('bags_quantity')
        if kwargs.get('type_place', None) is not None:
            extraction.type_place = kwargs.get('type_place')
        if kwargs.get('lot', None) is not None:
            extraction.lot = kwargs.get('lot')
        if kwargs.get('tubing', None) is not None:
            extraction.tubing = kwargs.get('tubing')
        if kwargs.get('weight', None) is not None:
            extraction.weight = kwargs.get('weight')
        if kwargs.get('arm', None) is not None:
            extraction.arm = kwargs.get('arm')
        if kwargs.get('barcode', None) is not None:
            extraction.barcode = kwargs.get('barcode')
        if kwargs.get('initial_time', None) is not None:
            extraction.initial_time = kwargs.get('initial_time')
        if kwargs.get('end_time', None) is not None:
            extraction.end_time = kwargs.get('end_time')
        if kwargs.get('employee_id', None) is not None:
            extraction.employee_id = kwargs.get('employee_id')
        if kwargs.get('total_time', None) is not None:
            extraction.total_time = kwargs.get('total_time')
        if kwargs.get('register_id', None) is not None:
            extraction.register_id = kwargs.get('register_id')
        if kwargs.get('observations', None) is not None:
            extraction.observations = kwargs.get('observations')
        if kwargs.get('register_at', None) is not None:
            extraction.register_at = kwargs.get('register_at')

        extraction.save()

        # TODO check this only date extraction is changed
        # itemfragmentations = ItemFragmentation.objects.filter(fragmentation__extraction=extraction)
        # for item in itemfragmentations:
        #     item.expiration_date = extraction.register_at + timedelta(days=item.typehemocomponent.expiration_day)
        #     item.save()

        return UpdateExtraction(extraction=extraction)


class CreateSelfExclusion(graphene.Mutation):
    selfexclusion = graphene.Field(lambda: SelfExclusionType)

    class Arguments:
        extraction_id = graphene.Int(required=True)
        employee_id = graphene.Int(required=True)
        register_id = graphene.Int(required=True)
        observations = graphene.String()
        register_at = graphene.Date(required=True)

    @permission_required(['extractions.add_selfexclusion'])
    def mutate(self, info, extraction_id, employee_id, register_id, register_at, **kwargs):
        _selfexclusion = SelfExclusion.objects.filter(extraction_id=extraction_id).first()

        if _selfexclusion is not None:
            raise ValueError('extraction_id: debe ser unico')

        selfexclusion = SelfExclusion(extraction_id=extraction_id, employee_id=employee_id, register_id=register_id,
                                      register_at=register_at)

        if kwargs.get('observations', None) is not None:
            selfexclusion.observations = kwargs.get('observations')

        selfexclusion.save()

        return CreateSelfExclusion(selfexclusion=selfexclusion)


class UpdateSelfExclusion(graphene.Mutation):
    selfexclusion = graphene.Field(lambda: SelfExclusionType)

    class Arguments:
        id = graphene.Int(required=True)
        extraction_id = graphene.Int()
        employee_id = graphene.Int()
        register_id = graphene.Int()
        observations = graphene.String()
        register_at = graphene.Date()

    @permission_required(['extractions.change_selfexclusion'])
    def mutate(self, info, id, **kwargs):
        selfexclusion = SelfExclusion.objects.filter(id=id).first()
        if not selfexclusion:
            raise ValueError("SelfExclusion not exists.")

        if kwargs.get('extraction_id', None) is not None:
            selfexclusion.extraction_id = kwargs.get('extraction_id')
        if kwargs.get('employee_id', None) is not None:
            selfexclusion.employee_id = kwargs.get('employee_id')
        if kwargs.get('register_id', None) is not None:
            selfexclusion.register_id = kwargs.get('register_id')
        if kwargs.get('observations', None) is not None:
            selfexclusion.observations = kwargs.get('observations')
        if kwargs.get('register_at', None) is not None:
            selfexclusion.register_at = kwargs.get('register_at')

        selfexclusion.save()

        return UpdateSelfExclusion(selfexclusion=selfexclusion)


class CreateTypeAdverseReaction(graphene.Mutation):
    typeadversereaction = graphene.Field(lambda: TypeAdverseReactionType)

    class Arguments:
        name = graphene.String(required=True)
        show_in_conventional = graphene.Boolean(required=True)
        show_in_apheresis = graphene.Boolean(required=True)
        level = graphene.String(required=True)

    @permission_required(['extractions.add_typeadversereaction'])
    def mutate(self, info, name, show_in_conventional, show_in_apheresis, level, **kwargs):
        typeadversereaction = TypeAdverseReaction(name=name, show_in_conventional=show_in_conventional,
                                                  show_in_apheresis=show_in_apheresis, level=level)
        typeadversereaction.save()

        return CreateTypeAdverseReaction(typeadversereaction=typeadversereaction)


class UpdateTypeAdverseReaction(graphene.Mutation):
    typeadversereaction = graphene.Field(lambda: TypeAdverseReactionType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        show_in_conventional = graphene.Boolean()
        show_in_apheresis = graphene.Boolean()
        level = graphene.String()

    @permission_required(['extractions.change_typeadversereaction'])
    def mutate(self, info, id, **kwargs):
        typeadversereaction = TypeAdverseReaction.objects.filter(id=id).first()
        if not typeadversereaction:
            raise ValueError("TypeAdverseReaction not exists.")

        if kwargs.get('name', None) is not None:
            typeadversereaction.name = kwargs.get('name')
        if kwargs.get('show_in_conventional', None) is not None:
            typeadversereaction.show_in_conventional = kwargs.get('show_in_conventional')
        if kwargs.get('show_in_apheresis', None) is not None:
            typeadversereaction.show_in_apheresis = kwargs.get('show_in_apheresis')
        if kwargs.get('level', None) is not None:
            typeadversereaction.level = kwargs.get('level')

        typeadversereaction.save()

        return UpdateTypeAdverseReaction(typeadversereaction=typeadversereaction)


class CreateAdverseReaction(graphene.Mutation):
    adversereaction = graphene.Field(lambda: AdverseReactionType)

    class Arguments:
        extraction_id = graphene.Int(required=True)
        type_id = generic.GenericScalar(required=True)
        extraction_place = graphene.String(required=True)
        evolution = graphene.String(required=True)
        detection = graphene.String(required=True)
        behavior_taken = graphene.String()
        employee_id = graphene.Int(required=True)
        observations = graphene.String()
        register_at = graphene.DateTime(required=True)

    @permission_required(['extractions.add_adversereaction'])
    def mutate(self, info, extraction_id, employee_id, extraction_place, evolution, detection, register_at, **kwargs):
        _adversereaction = AdverseReaction.objects.filter(extraction_id=extraction_id).first()

        if _adversereaction is not None:
            raise ValueError('extraction_id: debe ser unico')

        adversereaction = AdverseReaction(extraction_id=extraction_id, employee_id=employee_id,
                                          extraction_place=extraction_place, evolution=evolution, detection=detection,
                                          register_at=register_at)

        if kwargs.get('behavior_taken', None) is not None:
            adversereaction.behavior_taken = kwargs.get('behavior_taken')
        if kwargs.get('observations', None) is not None:
            adversereaction.observations = kwargs.get('observations')

        adversereaction.save()

        if kwargs.get('type_id', None) is not None:
            for item in kwargs.get('type_id'):
                adversereaction.type.add(item)

        return CreateAdverseReaction(adversereaction=adversereaction)


class UpdateAdverseReaction(graphene.Mutation):
    adversereaction = graphene.Field(lambda: AdverseReactionType)

    class Arguments:
        id = graphene.Int(required=True)
        extraction_id = graphene.Int()
        type_id = generic.GenericScalar()
        extraction_place = graphene.String()
        evolution = graphene.String()
        detection = graphene.String()
        behavior_taken = graphene.String()
        employee_id = graphene.Int()
        observations = graphene.String()
        register_at = graphene.DateTime()

    @permission_required(['extractions.change_adversereaction'])
    def mutate(self, info, id, **kwargs):
        adversereaction = AdverseReaction.objects.filter(id=id).first()
        if not adversereaction:
            raise ValueError("AdverseReaction not exists.")

        if kwargs.get('extraction_id', None) is not None:
            adversereaction.extraction_id = kwargs.get('extraction_id')
        if kwargs.get('extraction_place', None) is not None:
            adversereaction.extraction_place = kwargs.get('extraction_place')
        if kwargs.get('evolution', None) is not None:
            adversereaction.evolution = kwargs.get('evolution')
        if kwargs.get('detection', None) is not None:
            adversereaction.detection = kwargs.get('detection')
        if kwargs.get('behavior_taken', None) is not None:
            adversereaction.behavior_taken = kwargs.get('behavior_taken')
        if kwargs.get('employee_id', None) is not None:
            adversereaction.employee_id = kwargs.get('employee_id')
        if kwargs.get('observations', None) is not None:
            adversereaction.observations = kwargs.get('observations')
        if kwargs.get('register_at', None) is not None:
            adversereaction.register_at = kwargs.get('register_at')

        adversereaction.save()

        if kwargs.get('type_id', None) is not None:
            for item in kwargs.get('type_id'):
                adversereaction.type.add(item)

        return UpdateAdverseReaction(adversereaction=adversereaction)


class Mutation(graphene.ObjectType):
    create_extraction = CreateExtraction.Field()
    update_extraction = UpdateExtraction.Field()

    create_adversereaction = CreateAdverseReaction.Field()
    update_adversereaction = UpdateAdverseReaction.Field()

    create_typeadversereaction = CreateTypeAdverseReaction.Field()
    update_typeadversereaction = UpdateTypeAdverseReaction.Field()

    create_selfexclusion = CreateSelfExclusion.Field()
    update_selfexclusion = UpdateSelfExclusion.Field()
