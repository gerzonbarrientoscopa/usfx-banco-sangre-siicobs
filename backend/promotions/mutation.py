from __future__ import unicode_literals
import graphene

from graphql_jwt.decorators import permission_required

from promotions.models import Event
from promotions.schema import EventType


class CreateEvent(graphene.Mutation):
    event = graphene.Field(lambda: EventType)

    class Arguments:
        name = graphene.String(required=True)
        init_at = graphene.DateTime(required=True)
        end_at = graphene.DateTime()
        is_active = graphene.Boolean()

    @permission_required(['promotions.add_event'])
    def mutate(self, info, name, init_at, end_at, **kwargs):

        _event = Event.objects.filter(name=name, init_at=init_at, end_at=end_at)
        if _event:
            raise ValueError('Object already exist')

        event = Event(name=name, init_at=init_at, end_at=end_at)

        if kwargs.get('is_active', None) is not None:
            event.is_active = kwargs.get('is_active')

        event.save()

        return CreateEvent(event=event)


class UpdateEvent(graphene.Mutation):
    event = graphene.Field(lambda: EventType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        init_at = graphene.DateTime()
        end_at = graphene.DateTime()
        is_active = graphene.Boolean()

    @permission_required(['promotions.change_event'])
    def mutate(self, info, **kwargs):
        event = Event.objects.filter(id=kwargs.get('id')).first()

        if not event:
            raise ValueError("Event not exists.")

        if kwargs.get('name', None) is not None:
            event.name = kwargs.get('name')
        if kwargs.get('init_at', None) is not None:
            event.init_at = kwargs.get('init_at')
        if kwargs.get('end_at', None) is not None:
            event.end_at = kwargs.get('end_at')
        if kwargs.get('is_active', None) is not None:
            event.is_active = kwargs.get('is_active')

        event.save()

        return UpdateEvent(event=event)


class DeleteEvent(graphene.Mutation):
    event = graphene.Field(lambda: EventType)

    class Arguments:
        id = graphene.Int(required=True)

    @permission_required(['promotions.delete_event'])
    def mutate(self, info, **kwargs):
        event = Event.objects.get(id=kwargs.get('id'))
        if not event:
            raise ValueError("Event not exists.")

        event.delete()

        return DeleteEvent(event=event)


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()
