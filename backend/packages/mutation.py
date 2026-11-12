import graphene
from graphql_jwt.decorators import permission_required
from packages.models import TypeHemocomponent, Package, TypeDiscard
from packages.schema import TypeHemocomponentType, PackageType, TypeDiscardType


class CreateTypeHemocomponent(graphene.Mutation):
    typehemocomponent = graphene.Field(TypeHemocomponentType)

    class Arguments:
        name = graphene.String(required=True)
        acronym = graphene.String(required=True)
        expiration_day = graphene.Int()
        description = graphene.String()
        typecoagulation = graphene.String(required=True)
        temperature_save = graphene.String(required=True)
        position = graphene.Int()
        show_in_billing = graphene.Boolean(required=True)
        show_in_fragmentation = graphene.Boolean(required=True)
        show_in_request_release = graphene.Boolean(required=True)
        blocks_release_with_irregular_antibodies = graphene.Boolean()

    @permission_required(['packages.add_typehemocomponent'])
    def mutate(self, info, name, typecoagulation, acronym, temperature_save, show_in_billing, show_in_fragmentation,
               show_in_request_release, **kwargs):
        typehemocomponent = TypeHemocomponent(name=name, acronym=acronym, typecoagulation=typecoagulation,
                                              temperature_save=temperature_save,
                                              show_in_billing=show_in_billing,
                                              show_in_fragmentation=show_in_fragmentation,
                                              show_in_request_release=show_in_request_release)

        if kwargs.get('expiration_day', None) is not None:
            typehemocomponent.expiration_day = kwargs.get('expiration_day')
        if kwargs.get('description', None) is not None:
            typehemocomponent.description = kwargs.get('description')
        if kwargs.get('position', None) is not None:
            typehemocomponent.position = kwargs.get('position')
        if kwargs.get('blocks_release_with_irregular_antibodies', None) is not None:
            typehemocomponent.blocks_release_with_irregular_antibodies = kwargs.get(
                'blocks_release_with_irregular_antibodies')

        typehemocomponent.save()

        return CreateTypeHemocomponent(typehemocomponent=typehemocomponent)


class UpdateTypeHemocomponent(graphene.Mutation):
    typehemocomponent = graphene.Field(TypeHemocomponentType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        acronym = graphene.String()
        expiration_day = graphene.Int()
        description = graphene.String()
        typecoagulation = graphene.String()
        temperature_save = graphene.String()
        position = graphene.Int()
        show_in_billing = graphene.Boolean()
        show_in_fragmentation = graphene.Boolean()
        show_in_request_release = graphene.Boolean()
        blocks_release_with_irregular_antibodies = graphene.Boolean()

    @permission_required(['packages.change_typehemocomponent'])
    def mutate(self, info, id, **kwargs):
        typehemocomponent = TypeHemocomponent.objects.filter(id=id).first()
        if typehemocomponent is None:
            raise ValueError('TypeHemocomponent not found')

        if kwargs.get('name', None) is not None:
            typehemocomponent.name = kwargs.get('name')
        if kwargs.get('acronym', None) is not None:
            typehemocomponent.acronym = kwargs.get('acronym')
        if kwargs.get('expiration_day', None) is not None:
            typehemocomponent.expiration_day = kwargs.get('expiration_day')
        if kwargs.get('description', None) is not None:
            typehemocomponent.description = kwargs.get('description')
        if kwargs.get('typecoagulation', None) is not None:
            typehemocomponent.typecoagulation = kwargs.get('typecoagulation')
        if kwargs.get('temperature_save', None) is not None:
            typehemocomponent.temperature_save = kwargs.get('temperature_save')
        if kwargs.get('position', None) is not None:
            typehemocomponent.position = kwargs.get('position')
        if kwargs.get('show_in_billing', None) is not None:
            typehemocomponent.show_in_billing = kwargs.get('show_in_billing')
        if kwargs.get('show_in_fragmentation', None) is not None:
            typehemocomponent.show_in_fragmentation = kwargs.get('show_in_fragmentation')
        if kwargs.get('show_in_request_release', None) is not None:
            typehemocomponent.show_in_request_release = kwargs.get('show_in_request_release')
        if kwargs.get('blocks_release_with_irregular_antibodies', None) is not None:
            typehemocomponent.blocks_release_with_irregular_antibodies = kwargs.get(
                'blocks_release_with_irregular_antibodies')

        typehemocomponent.save()

        return UpdateTypeHemocomponent(typehemocomponent=typehemocomponent)


class CreatePackage(graphene.Mutation):
    package = graphene.Field(PackageType)

    class Arguments:
        typepatient_id = graphene.Int(required=True)
        code = graphene.String(required=True)
        typehemocomponent_id = graphene.Int(required=True)
        description = graphene.String()
        price = graphene.Float(required=True)

    @permission_required(['packages.add_package'])
    def mutate(self, info, typepatient_id, code, typehemocomponent_id, price, **kwargs):
        package = Package(typepatient_id=typepatient_id, code=code, typehemocomponent_id=typehemocomponent_id,
                          price=price)
        if kwargs.get('description', None) is not None:
            package.description = kwargs.get('description')

        package.save()

        return CreatePackage(package=package)


class UpdatePackage(graphene.Mutation):
    package = graphene.Field(PackageType)

    class Arguments:
        id = graphene.Int(required=True)
        typepatient_id = graphene.Int(required=True)
        code = graphene.String(required=True)
        typehemocomponent_id = graphene.Int(required=True)
        description = graphene.String()
        price = graphene.Float(required=True)

    @permission_required(['packages.change_package'])
    def mutate(self, info, id, **kwargs):
        package = Package.objects.filter(id=id).first()
        if package is None:
            raise ValueError('Package not found')

        if kwargs.get('typepatient_id', None) is not None:
            package.typepatient_id = kwargs.get('typepatient_id')
        if kwargs.get('code', None) is not None:
            package.code = kwargs.get('code')
        if kwargs.get('typehemocomponent_id', None) is not None:
            package.typehemocomponent_id = kwargs.get('typehemocomponent_id')
        if kwargs.get('description', None) is not None:
            package.description = kwargs.get('description')
        if kwargs.get('price', None) is not None:
            package.price = kwargs.get('price')

        package.save()

        return UpdatePackage(package=package)


class CreateTypeDiscard(graphene.Mutation):
    type_discard = graphene.Field(TypeDiscardType)

    class Arguments:
        name = graphene.String(required=True)
        typehemocomponent_id = graphene.Int(required=True)

    @permission_required(['packages.add_typediscard'])
    def mutate(self, info, name, typehemocomponent_id, **kwargs):
        type_discard = TypeDiscard(name=name, typehemocomponent_id=typehemocomponent_id)
        type_discard.save()

        return CreateTypeDiscard(type_discard=type_discard)


class UpdateTypeDiscard(graphene.Mutation):
    type_discard = graphene.Field(TypeDiscardType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)
        typehemocomponent_id = graphene.Int(required=True)

    @permission_required(['packages.change_typediscard'])
    def mutate(self, info, id, **kwargs):
        type_discard = TypeDiscard.objects.filter(id=id).first()
        if type_discard is None:
            raise ValueError('TypeDiscard not found')

        if kwargs.get('name', None) is not None:
            type_discard.name = kwargs.get('name')
        if kwargs.get('typehemocomponent_id', None) is not None:
            type_discard.typehemocomponent_id = kwargs.get('typehemocomponent_id')

        type_discard.save()

        return UpdateTypeDiscard(type_discard=type_discard)


class Mutation(graphene.ObjectType):
    create_typehemocomponent = CreateTypeHemocomponent.Field()
    update_typehemocomponent = UpdateTypeHemocomponent.Field()

    create_package = CreatePackage.Field()
    update_package = UpdatePackage.Field()

    create_typediscard = CreateTypeDiscard.Field()
    update_typediscard = UpdateTypeDiscard.Field()
