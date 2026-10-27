import graphene
from graphql_jwt.decorators import permission_required
from refreshments.models import Menu, ExtractionRefreshment
from refreshments.schema import MenuType, ExtractionRefreshmentType


class CreateMenu(graphene.Mutation):
    menu = graphene.Field(MenuType)

    class Arguments:
        name = graphene.String(required=True)
        only_volunteer = graphene.Boolean(required=True)

    @permission_required(['refreshments.add_menu'])
    def mutate(self, info, name, only_volunteer, **kwargs):
        menu = Menu(name=name, only_volunteer=only_volunteer)
        menu.save()

        return CreateMenu(menu=menu)


class UpdateMenu(graphene.Mutation):
    menu = graphene.Field(MenuType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        only_volunteer = graphene.Boolean()

    @permission_required(['refreshments.change_menu'])
    def mutate(self, info, id, **kwargs):
        menu = Menu.objects.filter(id=id).first()
        if menu is None:
            raise ValueError('Menu not found')

        if kwargs.get('name', None) is not None:
            menu.name = kwargs.get('name')
        if kwargs.get('only_volunteer', None) is not None:
            menu.only_volunteer = kwargs.get('only_volunteer')
        menu.save()

        return UpdateMenu(menu=menu)


class CreateExtractionRefreshment(graphene.Mutation):
    extractionrefreshment = graphene.Field(lambda: ExtractionRefreshmentType)

    class Arguments:
        extraction_id = graphene.Int(required=True)
        employee_id = graphene.Int(required=True)
        menu_id = graphene.Int(required=True)
        register_at = graphene.Date(required=True)

    @permission_required(['refreshments.add_extractionrefreshment'])
    def mutate(self, info, extraction_id, employee_id, menu_id, register_at, **kwargs):
        _extractionrefreshment = ExtractionRefreshment.objects.filter(extraction_id=extraction_id).first()

        if _extractionrefreshment is not None:
            raise ValueError('extraction_id: debe ser unico')

        extractionrefreshment = ExtractionRefreshment(extraction_id=extraction_id, employee_id=employee_id,
                                                      menu_id=menu_id, register_at=register_at)

        extractionrefreshment.save()

        return CreateExtractionRefreshment(extractionrefreshment=extractionrefreshment)


class UpdateExtractionRefreshment(graphene.Mutation):
    extractionrefreshment = graphene.Field(lambda: ExtractionRefreshmentType)

    class Arguments:
        id = graphene.Int(required=True)
        extraction_id = graphene.Int()
        employee_id = graphene.Int()
        menu_id = graphene.Int()
        register_at = graphene.Date()

    @permission_required(['refreshments.change_extractionrefreshment'])
    def mutate(self, info, id, **kwargs):
        extractionrefreshment = ExtractionRefreshment.objects.filter(id=id).first()
        if not extractionrefreshment:
            raise ValueError("ExtractionRefreshment not exists.")

        if kwargs.get('extraction_id', None) is not None:
            extractionrefreshment.extraction_id = kwargs.get('extraction_id')
        if kwargs.get('employee_id', None) is not None:
            extractionrefreshment.employee_id = kwargs.get('employee_id')
        if kwargs.get('menu_id', None) is not None:
            extractionrefreshment.menu_id = kwargs.get('menu_id')
        if kwargs.get('register_at', None) is not None:
            extractionrefreshment.register_at = kwargs.get('register_at')

        extractionrefreshment.save()

        return UpdateExtractionRefreshment(extractionrefreshment=extractionrefreshment)


class DeleteExtractionRefreshment(graphene.Mutation):
    extractionrefreshment = graphene.Field(ExtractionRefreshmentType)

    class Arguments:
        id = graphene.Int(required=True)

    @permission_required(['refreshments.delete_extractionrefreshment'])
    def mutate(self, info, id, **kwargs):
        extractionrefreshment = ExtractionRefreshment.objects.get(id=id)
        extractionrefreshment.delete()

        return DeleteExtractionRefreshment(extractionrefreshment=extractionrefreshment)


class Mutation(graphene.ObjectType):
    create_menu = CreateMenu.Field()
    update_menu = UpdateMenu.Field()

    create_extractionrefreshment = CreateExtractionRefreshment.Field()
    update_extractionrefreshment = UpdateExtractionRefreshment.Field()
    delete_extractionrefreshment = DeleteExtractionRefreshment.Field()
