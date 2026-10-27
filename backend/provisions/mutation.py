import graphene
from graphql_jwt.decorators import permission_required
from provisions.models import Provision
from provisions.schema import ProvisionType


class CreateProvision(graphene.Mutation):
    provision = graphene.Field(ProvisionType)

    class Arguments:
        donor_id = graphene.Int(required=True)
        patient_id = graphene.Int(required=True)
        register_at = graphene.Date()
        quantity = graphene.Int(required=True)
        description = graphene.String()
        employee_id = graphene.Int(required=True)

    @permission_required(['provisions.add_provision'])
    def mutate(self, info, donor_id, patient_id, quantity, employee_id, **kwargs):
        provision = Provision(donor_id=donor_id, patient_id=patient_id, quantity=quantity, employee_id=employee_id)

        if kwargs.get('register_at', None) is not None:
            provision.register_at = kwargs.get('register_at')
        if kwargs.get('description', None) is not None:
            provision.description = kwargs.get('description')

        provision.save()

        return CreateProvision(provision=provision)


class UpdateProvision(graphene.Mutation):
    provision = graphene.Field(ProvisionType)

    class Arguments:
        id = graphene.Int(required=True)
        donor_id = graphene.Int()
        patient_id = graphene.Int()
        register_at = graphene.Date()
        quantity = graphene.Int()
        description = graphene.String()
        employee_id = graphene.Int(required=True)

    @permission_required(['provisions.change_provision'])
    def mutate(self, info, id, **kwargs):
        provision = Provision.objects.filter(id=id).first()
        if provision is None:
            raise ValueError('Provision not found')

        if kwargs.get('donor_id', None) is not None:
            provision.donor_id = kwargs.get('donor_id')
        if kwargs.get('patient_id', None) is not None:
            provision.patient_id = kwargs.get('patient_id')
        if kwargs.get('quantity', None) is not None:
            provision.quantity = kwargs.get('quantity')
        if kwargs.get('employee_id', None) is not None:
            provision.employee_id = kwargs.get('employee_id')
        if kwargs.get('register_at', None) is not None:
            provision.register_at = kwargs.get('register_at')
        if kwargs.get('description', None) is not None:
            provision.description = kwargs.get('description')

        provision.save()

        return UpdateProvision(provision=provision)


class Mutation(graphene.ObjectType):
    create_provision = CreateProvision.Field()
    update_provision = UpdateProvision.Field()
