import datetime
import json

import graphene
from graphene.types import generic
from graphql_jwt.decorators import permission_required

from donors.models import Donor
from donations.models import Donation
from fragmentations.models import ItemFragmentation
from laboratories.models import Immunoserology, Immunohematology, SerologyProtocol
from laboratories.schema import ImmunoserologyType, ImmunohematologyType, SerologyProtocolType
from users.models import Employee
from users.util_users import get_fullname_employee


class CreateImmunoserology(graphene.Mutation):
    immunoserology = graphene.Field(lambda: ImmunoserologyType)

    class Arguments:
        donation_id = graphene.Int(required=True)
        hiv = graphene.String()
        hbsag = graphene.String()
        hvc = graphene.String()
        cheia = graphene.String()
        chagas_hai = graphene.String()
        rpr = graphene.String()
        observations = graphene.String()
        employee_id = graphene.Int(required=True)
        register_at = graphene.Date()

    @permission_required(['laboratories.add_immunoserology'])
    def mutate(self, info, donation_id, employee_id, **kwargs):
        donation = Donation.objects.get(id=donation_id)
        employee = Employee.objects.get(id=employee_id)
        immunoserology_obj = Immunoserology(donation=donation, employee=employee)

        if kwargs.get('hiv', None) is not None:
            immunoserology_obj.hiv = kwargs.get('hiv')
        if kwargs.get('hbsag', None) is not None:
            immunoserology_obj.hbsag = kwargs.get('hbsag')
        if kwargs.get('hvc', None) is not None:
            immunoserology_obj.hvc = kwargs.get('hvc')
        if kwargs.get('cheia', None) is not None:
            immunoserology_obj.cheia = kwargs.get('cheia')
        if kwargs.get('chagas_hai', None) is not None:
            immunoserology_obj.chagas_hai = kwargs.get('chagas_hai')
        if kwargs.get('rpr', None) is not None:
            immunoserology_obj.rpr = kwargs.get('rpr')
        if kwargs.get('observations', None) is not None:
            immunoserology_obj.observations = kwargs.get('observations')
        if kwargs.get('register_at', None) is not None:
            immunoserology_obj.register_at = kwargs.get('register_at')

        immunoserology_obj.save()

        if kwargs.get('hiv') == 'R' or kwargs.get('hbsag') == 'R' or kwargs.get('hvc') == 'R' or kwargs.get(
                'cheia') == 'R' or kwargs.get('chagas_hai') == 'R' or kwargs.get('rpr') == 'R':
            donor = Donor.objects.get(id=donation.donor.id)
            donor.can_donate = False
            donor.save()

        return CreateImmunoserology(immunoserology=immunoserology_obj)


class UpdateImmunoserology(graphene.Mutation):
    immunoserology = graphene.Field(lambda: ImmunoserologyType)

    class Arguments:
        id = graphene.Int(required=True)
        donation_id = graphene.Int()
        hiv = graphene.String()
        hbsag = graphene.String()
        hvc = graphene.String()
        cheia = graphene.String()
        chagas_hai = graphene.String()
        rpr = graphene.String()
        observations = graphene.String()
        employee_id = graphene.Int()
        register_at = graphene.Date()

    @permission_required(['laboratories.change_immunoserology'])
    def mutate(self, info, id, **kwargs):
        donation = Donation.objects.get(id=kwargs.get('donation_id'))
        employee = Employee.objects.get(id=kwargs.get('employee_id'))

        immunoserology_obj = Immunoserology.objects.filter(id=id).first()

        if immunoserology_obj is None:
            raise ValueError('Immunoserology not found')

        if kwargs.get('hiv') == 'R' or kwargs.get('hbsag') == 'R' or kwargs.get('hvc') == 'R' or kwargs.get(
                'cheia') == 'R' or kwargs.get('chagas_hai') == 'R' or kwargs.get('rpr') == 'R':
            donor = Donor.objects.get(id=donation.donor.id)
            donor.can_donate = False
            donor.save()

        if immunoserology_obj.history is not None:
            histories = immunoserology_obj.history
        else:
            histories = []

        if immunoserology_obj.hiv != kwargs.get('hiv'):
            log = {'property': 'hiv', 'before_value': immunoserology_obj.hiv, 'after_value': kwargs.get('hiv'),
                   'employee': get_fullname_employee(employee), 'employee_id': employee.id,
                   'created_at': str(datetime.datetime.now())}
            histories.insert(0, log)
        if immunoserology_obj.hbsag != kwargs.get('hbsag'):
            log = {'property': 'hbsag', 'before_value': immunoserology_obj.hbsag, 'after_value': kwargs.get('hbsag'),
                   'employee': get_fullname_employee(employee), 'employee_id': employee.id,
                   'created_at': str(datetime.datetime.now())}
            histories.insert(0, log)
        if immunoserology_obj.hvc != kwargs.get('hvc'):
            log = {'property': 'hvc', 'before_value': immunoserology_obj.hvc, 'after_value': kwargs.get('hvc'),
                   'employee': get_fullname_employee(employee), 'employee_id': employee.id,
                   'created_at': str(datetime.datetime.now())}
            histories.insert(0, log)
        if immunoserology_obj.cheia != kwargs.get('cheia'):
            log = {'property': 'cheia', 'before_value': immunoserology_obj.cheia, 'after_value': kwargs.get('cheia'),
                   'employee': get_fullname_employee(employee), 'employee_id': employee.id,
                   'created_at': str(datetime.datetime.now())}
            histories.insert(0, log)
        if immunoserology_obj.chagas_hai != kwargs.get('chagas_hai'):
            log = {'property': 'chagas_hai', 'before_value': immunoserology_obj.chagas_hai,
                   'after_value': kwargs.get('chagas_hai'),
                   'employee': get_fullname_employee(employee), 'employee_id': employee.id,
                   'created_at': str(datetime.datetime.now())}
            histories.insert(0, log)
        if immunoserology_obj.rpr != kwargs.get('rpr'):
            log = {'property': 'rpr', 'before_value': immunoserology_obj.rpr, 'after_value': kwargs.get('rpr'),
                   'employee': get_fullname_employee(employee), 'employee_id': employee.id,
                   'created_at': str(datetime.datetime.now())}
            histories.insert(0, log)

        immunoserology_obj.donation_id = donation

        if kwargs.get('hiv', None) is not None:
            immunoserology_obj.hiv = kwargs.get('hiv')
        if kwargs.get('hbsag', None) is not None:
            immunoserology_obj.hbsag = kwargs.get('hbsag')
        if kwargs.get('hvc', None) is not None:
            immunoserology_obj.hvc = kwargs.get('hvc')
        if kwargs.get('cheia', None) is not None:
            immunoserology_obj.cheia = kwargs.get('cheia')
        if kwargs.get('chagas_hai', None) is not None:
            immunoserology_obj.chagas_hai = kwargs.get('chagas_hai')
        if kwargs.get('rpr', None) is not None:
            immunoserology_obj.rpr = kwargs.get('rpr')

        immunoserology_obj.observations = kwargs.get('observations')
        immunoserology_obj.employee_id = kwargs.get('employee_id')
        immunoserology_obj.register_at = kwargs.get('register_at')
        immunoserology_obj.history = histories
        immunoserology_obj.save()

        return UpdateImmunoserology(immunoserology=immunoserology_obj)


class CreateImmunohematology(graphene.Mutation):
    immunohematology = graphene.Field(lambda: ImmunohematologyType)

    class Arguments:
        donation_id = graphene.Int(required=True)
        direct_abo = graphene.String()
        inverse_abo = graphene.String()
        factor_rh = graphene.String()
        phenotype = graphene.String()
        antikell = graphene.String()
        fsi = graphene.String()
        liss = graphene.String()
        alb = graphene.String()
        coombs = graphene.String()
        p2fsi = graphene.String()
        p2liss = graphene.String()
        p2alb = graphene.String()
        p2coombs = graphene.String()
        p3fsi = graphene.String()
        p3liss = graphene.String()
        p3alb = graphene.String()
        p3coombs = graphene.String()
        employee_id = graphene.Int(required=True)
        observations = graphene.String()
        register_at = graphene.Date()
        type_irregular_antibody_id = graphene.Int()

    @permission_required(['laboratories.add_immunohematology'])
    def mutate(self, info, donation_id, employee_id, **kwargs):
        donation = Donation.objects.get(id=donation_id)
        employee = Employee.objects.get(id=employee_id)
        immunohematology_obj = Immunohematology(donation=donation, employee=employee)

        if kwargs.get('inverse_abo', None) is not None:
            immunohematology_obj.inverse_abo = kwargs.get('inverse_abo')
        if kwargs.get('direct_abo', None) is not None:
            immunohematology_obj.direct_abo = kwargs.get('direct_abo')
        if kwargs.get('factor_rh', None) is not None:
            immunohematology_obj.factor_rh = kwargs.get('factor_rh')
        if kwargs.get('phenotype', None) is not None:
            immunohematology_obj.phenotype = kwargs.get('phenotype')
        if kwargs.get('antikell', None) is not None:
            immunohematology_obj.antikell = kwargs.get('antikell')
        if kwargs.get('fsi', None) is not None:
            immunohematology_obj.fsi = kwargs.get('fsi')
        if kwargs.get('liss', None) is not None:
            immunohematology_obj.liss = kwargs.get('liss')
        if kwargs.get('alb', None) is not None:
            immunohematology_obj.alb = kwargs.get('alb')
        if kwargs.get('coombs', None) is not None:
            immunohematology_obj.coombs = kwargs.get('coombs')
        if kwargs.get('p2fsi', None) is not None:
            immunohematology_obj.p2fsi = kwargs.get('p2fsi')
        if kwargs.get('p2liss', None) is not None:
            immunohematology_obj.p2liss = kwargs.get('p2liss')
        if kwargs.get('p2alb', None) is not None:
            immunohematology_obj.p2alb = kwargs.get('p2alb')
        if kwargs.get('p2coombs', None) is not None:
            immunohematology_obj.p2coombs = kwargs.get('p2coombs')
        if kwargs.get('p3fsi', None) is not None:
            immunohematology_obj.p3fsi = kwargs.get('p3fsi')
        if kwargs.get('p3liss', None) is not None:
            immunohematology_obj.p3liss = kwargs.get('p3liss')
        if kwargs.get('p3alb', None) is not None:
            immunohematology_obj.p3alb = kwargs.get('p3alb')
        if kwargs.get('p3coombs', None) is not None:
            immunohematology_obj.p3coombs = kwargs.get('p3coombs')
        if kwargs.get('observations', None) is not None:
            immunohematology_obj.observations = kwargs.get('observations')
        if kwargs.get('register_at', None) is not None:
            immunohematology_obj.register_at = kwargs.get('register_at')
        immunohematology_obj.save()

        if kwargs.get('type_irregular_antibody_id', None) is not None:
            ItemFragmentation.objects.filter(
                fragmentation__extraction__donation__immunohematology__id=immunohematology_obj.id).update(
                type_irregular_antibody_id=kwargs.get('type_irregular_antibody_id'))

        Donor.objects.filter(donations__id=immunohematology_obj.donation.id).update(
            group_abo=immunohematology_obj.direct_abo, factor_rh=immunohematology_obj.factor_rh)

        return CreateImmunohematology(immunohematology=immunohematology_obj)


class UpdateImmunohematology(graphene.Mutation):
    immunohematology = graphene.Field(lambda: ImmunohematologyType)

    class Arguments:
        id = graphene.Int(required=True)
        donation_id = graphene.Int()
        direct_a = graphene.String()
        direct_b = graphene.String()
        direct_ab = graphene.String()
        inverse_gra = graphene.String()
        inverse_abo = graphene.String()
        direct_abo = graphene.String()
        factor_rh = graphene.String()
        phenotype = graphene.String()
        version = graphene.String()
        antikell = graphene.String()
        fsi = graphene.String()
        liss = graphene.String()
        alb = graphene.String()
        bro = graphene.String()
        coombs = graphene.String()
        p2fsi = graphene.String()
        p2liss = graphene.String()
        p2alb = graphene.String()
        p2coombs = graphene.String()
        p3fsi = graphene.String()
        p3liss = graphene.String()
        p3alb = graphene.String()
        p3pt = graphene.String()
        p3coombs = graphene.String()
        employee_id = graphene.Int()
        observations = graphene.String()
        register_at = graphene.Date()
        type_irregular_antibody_id = graphene.Int()

    @permission_required(['laboratories.change_immunohematology'])
    def mutate(self, info, id, **kwargs):
        immunohematology_obj = Immunohematology.objects.filter(id=id).first()

        if immunohematology_obj is None:
            raise ValueError('Immunohematology not found')

        if kwargs.get('donation_id', None) is not None:
            immunohematology_obj.donation_id = kwargs.get('donation_id')
        if kwargs.get('employee_id', None) is not None:
            immunohematology_obj.employee_id = kwargs.get('employee_id')
        if kwargs.get('direct_a', None) is not None:
            immunohematology_obj.direct_a = kwargs.get('direct_a')
        if kwargs.get('direct_b', None) is not None:
            immunohematology_obj.direct_b = kwargs.get('direct_b')
        if kwargs.get('direct_ab', None) is not None:
            immunohematology_obj.direct_ab = kwargs.get('direct_ab')
        if kwargs.get('inverse_gra', None) is not None:
            immunohematology_obj.inverse_gra = kwargs.get('inverse_gra')
        if kwargs.get('inverse_abo', None) is not None:
            immunohematology_obj.inverse_abo = kwargs.get('inverse_abo')
        if kwargs.get('direct_abo', None) is not None:
            immunohematology_obj.direct_abo = kwargs.get('direct_abo')
        if kwargs.get('factor_rh', None) is not None:
            immunohematology_obj.factor_rh = kwargs.get('factor_rh')
        if kwargs.get('phenotype', None) is not None:
            immunohematology_obj.phenotype = kwargs.get('phenotype')
        if kwargs.get('version', None) is not None:
            immunohematology_obj.version = kwargs.get('version')
        if kwargs.get('antikell', None) is not None:
            immunohematology_obj.antikell = kwargs.get('antikell')
        if kwargs.get('fsi', None) is not None:
            immunohematology_obj.fsi = kwargs.get('fsi')
        if kwargs.get('liss', None) is not None:
            immunohematology_obj.liss = kwargs.get('liss')
        if kwargs.get('alb', None) is not None:
            immunohematology_obj.alb = kwargs.get('alb')
        if kwargs.get('bro', None) is not None:
            immunohematology_obj.bro = kwargs.get('bro')
        if kwargs.get('coombs', None) is not None:
            immunohematology_obj.coombs = kwargs.get('coombs')
        if kwargs.get('p2fsi', None) is not None:
            immunohematology_obj.p2fsi = kwargs.get('p2fsi')
        if kwargs.get('p2liss', None) is not None:
            immunohematology_obj.p2liss = kwargs.get('p2liss')
        if kwargs.get('p2alb', None) is not None:
            immunohematology_obj.p2alb = kwargs.get('p2alb')
        if kwargs.get('p2coombs', None) is not None:
            immunohematology_obj.p2coombs = kwargs.get('p2coombs')
        if kwargs.get('p3fsi', None) is not None:
            immunohematology_obj.p3fsi = kwargs.get('p3fsi')
        if kwargs.get('p3liss', None) is not None:
            immunohematology_obj.p3liss = kwargs.get('p3liss')
        if kwargs.get('p3alb', None) is not None:
            immunohematology_obj.p3alb = kwargs.get('p3alb')
        if kwargs.get('p3pt', None) is not None:
            immunohematology_obj.p3pt = kwargs.get('p3pt')
        if kwargs.get('p3coombs', None) is not None:
            immunohematology_obj.p3coombs = kwargs.get('p3coombs')
        if kwargs.get('observations', None) is not None:
            immunohematology_obj.observations = kwargs.get('observations')
        if kwargs.get('register_at', None) is not None:
            immunohematology_obj.register_at = kwargs.get('register_at')
        immunohematology_obj.save()

        if kwargs.get('type_irregular_antibody_id', None) is not None:
            ItemFragmentation.objects.filter(
                fragmentation__extraction__donation__immunohematology__id=immunohematology_obj.id).update(
                type_irregular_antibody_id=kwargs.get('type_irregular_antibody_id'))

        Donor.objects.filter(donations__id=immunohematology_obj.donation.id).update(
            group_abo=immunohematology_obj.direct_abo, factor_rh=immunohematology_obj.factor_rh)

        return UpdateImmunohematology(immunohematology=immunohematology_obj)


class CreateSerologyProtocol(graphene.Mutation):
    serologyprotocol = graphene.Field(SerologyProtocolType)

    class Arguments:
        method = graphene.String(required=True)
        kit = graphene.String(required=True)
        due_date_at = graphene.Date(required=True)
        lot = graphene.String(required=True)
        industry = graphene.String(required=True)
        test = graphene.Int(required=True)
        values = generic.GenericScalar(required=True)
        type = graphene.String(required=True)
        cutt_off = graphene.String()
        cutt_off_max = graphene.String()
        cutt_off_min = graphene.String()
        employee_id = graphene.Int(required=True)
        register_at = graphene.Date()

    @permission_required(['laboratories.add_serologyprotocol'])
    def mutate(self, info, method, employee_id, kit, due_date_at, lot, industry, test, values, type, **kwargs):
        serologyprotocol = SerologyProtocol(method=method, kit=kit, employee_id=employee_id, due_date_at=due_date_at,
                                            lot=lot, test=test, industry=industry, values=values, type=type)

        if kwargs.get('cutt_off', None) is not None:
            serologyprotocol.cutt_off = kwargs.get('cutt_off')
        if kwargs.get('cutt_off_max', None) is not None:
            serologyprotocol.cutt_off_max = kwargs.get('cutt_off_max')
        if kwargs.get('cutt_off_min', None) is not None:
            serologyprotocol.cutt_off_min = kwargs.get('cutt_off_min')
        if kwargs.get('register_at', None) is not None:
            serologyprotocol.register_at = kwargs.get('register_at')

        serologyprotocol.save()

        return CreateSerologyProtocol(serologyprotocol=serologyprotocol)


class UpdateSerologyProtocol(graphene.Mutation):
    serologyprotocol = graphene.Field(SerologyProtocolType)

    class Arguments:
        id = graphene.Int(required=True)
        method = graphene.String()
        kit = graphene.String()
        due_date_at = graphene.Date()
        lot = graphene.String()
        industry = graphene.String()
        test = graphene.Int()
        values = generic.GenericScalar()
        type = graphene.String()
        cutt_off = graphene.String()
        cutt_off_max = graphene.String()
        cutt_off_min = graphene.String()
        employee_id = graphene.Int()
        register_at = graphene.Date()

    @permission_required(['laboratories.change_serologyprotocol'])
    def mutate(self, info, id, **kwargs):
        serologyprotocol = SerologyProtocol.objects.filter(id=id).first()
        if serologyprotocol is None:
            raise ValueError('SerologyProtocol not found')

        if kwargs.get('method', None) is not None:
            serologyprotocol.method = kwargs.get('method')
        if kwargs.get('kit', None) is not None:
            serologyprotocol.kit = kwargs.get('kit')
        if kwargs.get('due_date_at', None) is not None:
            serologyprotocol.due_date_at = kwargs.get('due_date_at')
        if kwargs.get('lot', None) is not None:
            serologyprotocol.lot = kwargs.get('lot')
        if kwargs.get('industry', None) is not None:
            serologyprotocol.industry = kwargs.get('industry')
        if kwargs.get('test', None) is not None:
            serologyprotocol.test = kwargs.get('test')
        if kwargs.get('values', None) is not None:
            serologyprotocol.values = kwargs.get('values')
        if kwargs.get('type', None) is not None:
            serologyprotocol.type = kwargs.get('type')
        if kwargs.get('cutt_off', None) is not None:
            serologyprotocol.cutt_off = kwargs.get('cutt_off')
        if kwargs.get('cutt_off_max', None) is not None:
            serologyprotocol.cutt_off_max = kwargs.get('cutt_off_max')
        if kwargs.get('cutt_off_min', None) is not None:
            serologyprotocol.cutt_off_min = kwargs.get('cutt_off_min')
        if kwargs.get('employee_id', None) is not None:
            serologyprotocol.employee_id = kwargs.get('employee_id')
        if kwargs.get('register_at', None) is not None:
            serologyprotocol.register_at = kwargs.get('register_at')

        serologyprotocol.save()

        return UpdateSerologyProtocol(serologyprotocol=serologyprotocol)


class DeleteSerologyProtocol(graphene.Mutation):
    serologyprotocol = graphene.Field(SerologyProtocolType)

    class Arguments:
        id = graphene.Int(required=True)

    @permission_required(['laboratories.delete_serologyprotocol'])
    def mutate(self, info, id, **kwargs):
        serologyprotocol = SerologyProtocol.objects.get(id=id)
        serologyprotocol.delete()

        return DeleteSerologyProtocol(serologyprotocol=serologyprotocol)


class Mutation(graphene.ObjectType):
    create_immunoserology = CreateImmunoserology.Field()
    update_immunoserology = UpdateImmunoserology.Field()

    create_immunohematology = CreateImmunohematology.Field()
    update_immunohematology = UpdateImmunohematology.Field()

    create_serologyprotocol = CreateSerologyProtocol.Field()
    update_serologyprotocol = UpdateSerologyProtocol.Field()
    delete_serologyprotocol = DeleteSerologyProtocol.Field()
