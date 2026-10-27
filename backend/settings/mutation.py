from __future__ import unicode_literals
import graphene

from graphql_jwt.decorators import permission_required

from settings.models import Reason
from settings.schema import ReasonType


class CreateReason(graphene.Mutation):
    reason = graphene.Field(ReasonType)

    class Arguments:
        name = graphene.String(required=True)
        type = graphene.String(required=True)

    @permission_required(['donors.add_reason'])
    def mutate(self, info, name, type, **kwargs):
        reason = Reason(name=name, type=type)
        reason.save()

        return CreateReason(reason=reason)


class UpdateReason(graphene.Mutation):
    reason = graphene.Field(ReasonType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)
        type = graphene.String(required=True)

    @permission_required(['donors.change_reason'])
    def mutate(self, info, id, **kwargs):
        reason = Reason.objects.filter(id=id).first()
        if reason is None:
            raise ValueError('Reason not found')

        if kwargs.get('name', None) is not None:
            reason.name = kwargs.get('name')
        if kwargs.get('type', None) is not None:
            reason.type = kwargs.get('type')
        reason.save()

        return UpdateReason(reason=reason)


class Mutation(graphene.ObjectType):
    create_reason = CreateReason.Field()
    update_reason = UpdateReason.Field()
