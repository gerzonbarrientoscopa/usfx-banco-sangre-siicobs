from __future__ import unicode_literals

import datetime
import json

import graphene
from django.db.models import Q
from graphene.types import generic
from graphql_jwt.decorators import permission_required

from donations.models import Donation
from donors.models import Donor, DonorHistory
from donors.schema_donations import DonorType, DonorHistoryType
from users.templatetags.utils import calculate_age
from users.util_users import get_fullname_employee


def is_using_code(code_other, id, update=False):
    code_other_array = code_other.split(',')

    for co in code_other_array:
        conditions = Q()
        conditions.add((Q(code__icontains=co) | Q(code_other__icontains=co)), conditions.connector)
        if update:
            donor = Donor.objects.filter(conditions).exclude(id=id)
        else:
            donor = Donor.objects.filter(conditions)
        if donor:
            return True
    return False


class CreateDonor(graphene.Mutation):
    donor = graphene.Field(lambda: DonorType)

    class Arguments:
        code = graphene.String(required=True)
        code_other = graphene.String()
        first_name = graphene.String(required=True)
        middle_name = graphene.String()
        last_name = graphene.String(required=True)
        birth_date = graphene.Date(required=True)
        gender = graphene.String(required=True)
        ci = graphene.String()
        ci_extension = graphene.String()
        civil_status = graphene.String()
        is_volunteer = graphene.Boolean()
        country = graphene.String(required=True)
        residence = graphene.String(required=True)
        zone = graphene.String()
        province = graphene.String()
        phone = graphene.Int()
        mobile_phone = graphene.Int()
        family_phone = graphene.Int()
        profession = graphene.String()
        degree_instruction = graphene.String(required=True)
        department = graphene.String(required=True)
        job = graphene.String()
        job_address = graphene.String()
        email = graphene.String()

    @permission_required(['donors.add_donor'])
    def mutate(self, info, code, first_name, last_name, birth_date, gender, country, residence, degree_instruction,
               department, **kwargs):

        donor = Donor(code=code, first_name=first_name, last_name=last_name, birth_date=birth_date, gender=gender,
                      country=country, residence=residence, degree_instruction=degree_instruction,
                      department=department)

        if kwargs.get('civil_status', None) is not None:
            donor.civil_status = kwargs.get('civil_status')
        if kwargs.get('middle_name', None) is not None:
            donor.middle_name = kwargs.get('middle_name')
        if kwargs.get('is_volunteer', None) is not None:
            donor.is_volunteer = kwargs.get('is_volunteer')
        if kwargs.get('zone', None) is not None:
            donor.zone = kwargs.get('zone')
        if kwargs.get('province', None) is not None:
            donor.province = kwargs.get('province')
        if kwargs.get('phone', None) is not None:
            donor.phone = kwargs.get('phone')
        if kwargs.get('mobile_phone', None) is not None:
            donor.mobile_phone = kwargs.get('mobile_phone')
        if kwargs.get('family_phone', None) is not None:
            donor.family_phone = kwargs.get('family_phone')
        if kwargs.get('profession', None) is not None:
            donor.profession = kwargs.get('profession')
        if kwargs.get('job', None) is not None:
            donor.job = kwargs.get('job')
        if kwargs.get('job_address', None) is not None:
            donor.job_address = kwargs.get('job_address')
        if kwargs.get('email', None) is not None:
            donor.email = kwargs.get('email')
        if kwargs.get('ci', None) is not None:
            donor.ci = kwargs.get('ci')
        if kwargs.get('ci_extension', None) is not None:
            donor.ci_extension = kwargs.get('ci_extension')

        if kwargs.get('code_other', None) is not None and kwargs.get('code_other') != '':
            if is_using_code(kwargs.get('code_other'), None, False):
                raise ValueError('code_other: El código secundario ya está en uso')
            donor.code_other = kwargs.get('code_other')

        donor.save()

        return CreateDonor(donor=donor)


class UpdateDonor(graphene.Mutation):
    donor = graphene.Field(lambda: DonorType)

    class Arguments:
        id = graphene.Int(required=True)
        code = graphene.String()
        code_other = graphene.String()
        first_name = graphene.String()
        middle_name = graphene.String()
        last_name = graphene.String()
        birth_date = graphene.Date()
        gender = graphene.String()
        ci = graphene.String()
        ci_extension = graphene.String()
        civil_status = graphene.String()
        is_volunteer = graphene.Boolean()
        country = graphene.String()
        residence = graphene.String()
        zone = graphene.String()
        province = graphene.String()
        phone = graphene.Int()
        mobile_phone = graphene.Int()
        family_phone = graphene.Int()
        profession = graphene.String()
        degree_instruction = graphene.String()
        department = graphene.String()
        job = graphene.String()
        job_address = graphene.String()
        email = graphene.String()

    @permission_required(['donors.change_donor'])
    def mutate(self, info, id, **kwargs):
        donor = Donor.objects.filter(id=id).first()

        if not donor:
            raise ValueError("Donor not exists.")

        if kwargs.get('code', None) is not None:
            donor.code = kwargs.get('code')
        if kwargs.get('first_name', None) is not None:
            donor.first_name = kwargs.get('first_name')
        if kwargs.get('middle_name', None) is not None:
            donor.middle_name = kwargs.get('middle_name')
        if kwargs.get('last_name', None) is not None:
            donor.last_name = kwargs.get('last_name')
        if kwargs.get('birth_date', None) is not None:
            donor.birth_date = kwargs.get('birth_date')
        if kwargs.get('gender', None) is not None:
            donor.gender = kwargs.get('gender')
        if kwargs.get('civil_status', None) is not None:
            donor.civil_status = kwargs.get('civil_status')
        if kwargs.get('is_volunteer', None) is not None:
            donor.is_volunteer = kwargs.get('is_volunteer')
        if kwargs.get('country', None) is not None:
            donor.country = kwargs.get('country')
        if kwargs.get('residence', None) is not None:
            donor.residence = kwargs.get('residence')
        if kwargs.get('zone', None) is not None:
            donor.zone = kwargs.get('zone')
        if kwargs.get('province', None) is not None:
            donor.province = kwargs.get('province')
        if kwargs.get('phone', None) is not None:
            donor.phone = kwargs.get('phone')
        if kwargs.get('mobile_phone', None) is not None:
            donor.mobile_phone = kwargs.get('mobile_phone')
        if kwargs.get('family_phone', None) is not None:
            donor.family_phone = kwargs.get('family_phone')
        if kwargs.get('profession', None) is not None:
            donor.profession = kwargs.get('profession')
        if kwargs.get('degree_instruction', None) is not None:
            donor.degree_instruction = kwargs.get('degree_instruction')
        if kwargs.get('department', None) is not None:
            donor.department = kwargs.get('department')
        if kwargs.get('job', None) is not None:
            donor.job = kwargs.get('job')
        if kwargs.get('job_address', None) is not None:
            donor.job_address = kwargs.get('job_address')
        if kwargs.get('email', None) is not None:
            donor.email = kwargs.get('email')
        if kwargs.get('ci', None) is not None:
            donor.ci = kwargs.get('ci')
        if kwargs.get('ci_extension', None) is not None:
            donor.ci_extension = kwargs.get('ci_extension')

        if kwargs.get('code_other', None) is not None and kwargs.get('code_other') != '':
            if is_using_code(kwargs.get('code_other'), id, True):
                raise ValueError('code_other: El código secundario ya está en uso')
            donor.code_other = kwargs.get('code_other')

        donor.save()

        return UpdateDonor(donor=donor)


class JoinDonor(graphene.Mutation):
    donor = graphene.Field(lambda: DonorType)

    class Arguments:
        id = graphene.Int(required=True)
        items = generic.GenericScalar(required=True)

    @permission_required(['donors.change_donor'])
    def mutate(self, info, id, items):
        donor_main = Donor.objects.filter(id=id).first()
        if not donor_main:
            raise ValueError("Donor not exists.")

        if items:
            donor_main = Donor.objects.get(id=donor_main.id)
            donor_codes = []
            if donor_main.code_other:
                donor_codes = donor_main.code_other.split(',')

            for bp in items:
                donor = Donor.objects.get(id=bp.get('id'))
                Donation.objects.filter(donor_id=donor.id).update(donor_id=donor_main.id)
                Provision.objects.filter(donor_id=donor.id).update(donor_id=donor_main.id)

                donor_codes.append(donor.code)
                donor.delete()

            donor_main.code_other = ','.join(map(str, donor_codes))
            donor_main.save()

        return JoinDonor(donor=donor_main)


def update_donor(rejected):
    if rejected.reason.type == 'PE':
        donor = Donor.objects.get(id=rejected.donation.donor.id)

        if donor and donor.can_donate:
            donor.can_donate = False
            donor.save()


class CreateDonorHistory(graphene.Mutation):
    donorhistory = graphene.Field(lambda: DonorHistoryType)

    class Arguments:
        donor_id = graphene.Int(required=True)
        reason = graphene.String(required=True)
        employee_id = graphene.Int(required=True)
        register_at = graphene.Date(required=True)

    @permission_required(['donors.add_donorhistory'])
    def mutate(self, info, donor_id, reason, register_at, employee_id, **kwargs):
        donorhistory = DonorHistory(donor_id=donor_id, reason=reason, register_at=register_at, employee_id=employee_id)
        donorhistory.save()

        Donor.objects.filter(id=donor_id).update(can_donate=True)

        return CreateDonorHistory(donorhistory=donorhistory)


class Mutation(graphene.ObjectType):
    create_donor = CreateDonor.Field()
    update_donor = UpdateDonor.Field()
    join_donor = JoinDonor.Field()

    create_donorhistory = CreateDonorHistory.Field()
