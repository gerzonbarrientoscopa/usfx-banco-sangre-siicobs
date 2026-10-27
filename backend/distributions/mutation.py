from __future__ import unicode_literals
import graphene
from datetime import datetime
from graphql_jwt.decorators import permission_required

from distributions.models import DistributionItemFragmentation, Distribution, DistributionItemFragmentationRefunded
from distributions.schema import DistributionType, DistributionItemFragmentationRefundedType


class CreateItemDistributionRefunded(graphene.Mutation):
    distribution_item_fragmentation_refunded = graphene.Field(lambda: DistributionItemFragmentationRefundedType)

    class Arguments:
        id = graphene.Int(required=True)
        reason = graphene.String(required=True)

    @permission_required(['distributions.add_distributionitemfragmentationrefunded'])
    def mutate(self, info, id, reason, **kwargs):
        item = DistributionItemFragmentation.objects.filter(id=id).first()
        item_refunded = None
        if not item:
            raise ValueError("Item Distribution not exists.")
        if item:
            item_refunded = DistributionItemFragmentationRefunded(distributionitemfragmentation_id=id,
                                                                  reason=reason)
            item_refunded.save()

        distribution = Distribution.objects.get(id=item.distribution.id)

        item_lenght = DistributionItemFragmentation.objects.filter(distribution_id=distribution.id).count()
        items = DistributionItemFragmentation.objects.filter(distribution_id=distribution.id).exclude(
            distributionitemfragmentationrefunded=None)

        if len(items) != item_lenght:
            distribution.status = 'PARTIAL_REFUNDED'
            distribution.save()
        else:
            distribution.status = 'REFUNDED'
            distribution.save()

        return CreateItemDistributionRefunded(distribution_item_fragmentation_refunded=item_refunded)


class DistributionItemInput(graphene.InputObjectType):
    id = graphene.Int(required=True)


class CreateDistribution(graphene.Mutation):
    distribution = graphene.Field(lambda: DistributionType)

    class Arguments:
        patient_id = graphene.Int()
        medical_id = graphene.Int(required=True)
        institution_id = graphene.Int(required=True)
        type_payment = graphene.String(required=True)
        employee_id = graphene.Int(required=True)
        service_transfunctional = graphene.String()
        is_donation = graphene.Boolean()
        observations = graphene.String()
        register_at = graphene.DateTime(required=True)
        itemfragmentations = graphene.List(DistributionItemInput)
        status = graphene.String()

    @permission_required(['distributions.add_distribution'])
    def mutate(self, info, register_at, medical_id, institution_id, is_donation, type_payment, employee_id, **kwargs):
        distribution = Distribution(register_at=register_at, medical_id=medical_id, institution_id=institution_id,
                                    is_donation=is_donation, type_payment=type_payment, employee_id=employee_id,
                                    status='IN_PROGRESS')

        if kwargs.get('patient_id', None) is not None:
            distribution.patient_id = kwargs.get('patient_id')
        if kwargs.get('service_transfunctional', None) is not None:
            distribution.service_transfunctional = kwargs.get('transfunctional')
        if kwargs.get('observations', None) is not None:
            distribution.observations = kwargs.get('observations')

        distribution.save()

        if kwargs.get('itemfragmentations', None) is not None:
            items = kwargs.get('itemfragmentations')
            DistributionItemFragmentation.objects.filter(distribution_id=distribution.id).delete()

            for item in items:
                detail = DistributionItemFragmentation(distribution_id=distribution.id, itemfragmentation_id=item.id)
                detail.save()

        return CreateDistribution(distribution=distribution)


class UpdateDistribution(graphene.Mutation):
    distribution = graphene.Field(lambda: DistributionType)

    class Arguments:
        id = graphene.Int(required=True)
        patient_id = graphene.Int()
        medical_id = graphene.Int()
        service_transfunctional = graphene.String()
        institution_id = graphene.Int()
        is_donation = graphene.Boolean()
        type_payment = graphene.String()
        employee_id = graphene.Int()
        observations = graphene.String()
        status = graphene.String()
        register_at = graphene.DateTime()
        itemfragmentations = graphene.List(DistributionItemInput)

    @permission_required(['distributions.change_distribution'])
    def mutate(self, info, id, **kwargs):
        distribution = Distribution.objects.filter(id=id).first()
        if not distribution:
            raise ValueError("Distribution not exists.")

        if kwargs.get('medical_id', None) is not None:
            distribution.medical_id = kwargs.get('medical_id')
        if kwargs.get('institution_id', None) is not None:
            distribution.institution_id = kwargs.get('institution_id')
        if kwargs.get('is_donation', None) is not None:
            distribution.is_donation = kwargs.get('is_donation')
        if kwargs.get('observations', None) is not None:
            distribution.observations = kwargs.get('observations')
        if kwargs.get('type_payment', None) is not None:
            distribution.type_payment = kwargs.get('type_payment')

        if kwargs.get('status', None) is not None:
            if kwargs.get('itemfragmentations') is not None and len(
                    kwargs.get('itemfragmentations')) == 0 and kwargs.get('status') != 'CANCELED':
                distribution.status = 'NEW'
            else:
                distribution.status = kwargs.get('status')

        if kwargs.get('employee_id', None) is not None:
            distribution.employee_id = kwargs.get('employee_id')
        if kwargs.get('service_transfunctional', None) is not None:
            distribution.service_transfunctional = kwargs.get('transfunctional')
        if kwargs.get('observations', None) is not None:
            distribution.observations = kwargs.get('observations')
        if kwargs.get('register_at', None) is not None:
            distribution.register_at = kwargs.get('register_at')

        distribution.save()
        if distribution.status == 'CANCELED':
            distribution_item_fragmentation = DistributionItemFragmentation.objects.filter(
                distribution_id=distribution.id)
            for dif in distribution_item_fragmentation:
                difr = DistributionItemFragmentationRefunded(distributionitemfragmentation_id=dif.id,
                                                             reason='CANCELADO')
                difr.save()

        if distribution.status == 'DELIVERED':
            distribution.delivered_at = datetime.now()
            distribution.save()

        if kwargs.get('itemfragmentations', None) is not None:
            items = kwargs.get('itemfragmentations')
            DistributionItemFragmentation.objects.filter(distribution_id=distribution.id).delete()

            for item in items:
                detail = DistributionItemFragmentation(distribution_id=distribution.id, itemfragmentation_id=item.id)
                detail.save()

        return UpdateDistribution(distribution=distribution)


class Mutation(graphene.ObjectType):
    create_distribution_item_fragmentation_refunded = CreateItemDistributionRefunded.Field()

    create_distribution = CreateDistribution.Field()
    update_distribution = UpdateDistribution.Field()
