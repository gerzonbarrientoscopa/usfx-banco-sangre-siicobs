from __future__ import unicode_literals
import graphene

from graphql_jwt.decorators import permission_required

from users.models import Institution, Employee, Patient, Medical
from users.schema import InstitutionType, EmployeeType, UserType, PatientType, MedicalType
from django.contrib.auth.models import User, Group


class CreateInstitution(graphene.Mutation):
    institution = graphene.Field(lambda: InstitutionType)

    class Arguments:
        name = graphene.String(required=True)
        department = graphene.String(required=True)
        nit = graphene.String()
        nro_authorization = graphene.String()
        dosage_key = graphene.String()
        address = graphene.String()
        phone = graphene.Int()
        type = graphene.String()

    @permission_required(['users.add_institution'])
    def mutate(self, info, name, department, **kwargs):
        institution = Institution(name=name, department=department)

        if kwargs.get('nit', None) is not None:
            institution.nit = kwargs.get('nit')
        if kwargs.get('nro_authorization', None) is not None:
            institution.nro_authorization = kwargs.get('nro_authorization')
        if kwargs.get('dosage_key', None) is not None:
            institution.dosage_key = kwargs.get('dosage_key')
        if kwargs.get('address', None) is not None:
            institution.address = kwargs.get('address')
        if kwargs.get('phone', None) is not None:
            institution.phone = kwargs.get('phone')
        if kwargs.get('type', None) is not None:
            institution.type = kwargs.get('type')
        institution.save()

        return CreateInstitution(institution=institution)


class UpdateInstitution(graphene.Mutation):
    institution = graphene.Field(lambda: InstitutionType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        nit = graphene.String()
        nro_authorization = graphene.String()
        dosage_key = graphene.String()
        logo = graphene.String()
        address = graphene.String()
        phone = graphene.Int()
        department = graphene.String()
        type = graphene.String()

    @permission_required(['users.change_institution'])
    def mutate(self, info, id, **kwargs):
        institution = Institution.objects.filter(id=id).first()

        if not institution:
            raise ValueError("Institution not exists.")

        if kwargs.get('name', None) is not None:
            institution.name = kwargs.get('name')
        if kwargs.get('department', None) is not None:
            institution.department = kwargs.get('department')
        if kwargs.get('nit', None) is not None:
            institution.nit = kwargs.get('nit')
        if kwargs.get('nro_authorization', None) is not None:
            institution.nro_authorization = kwargs.get('nro_authorization')
        if kwargs.get('dosage_key', None) is not None:
            institution.dosage_key = kwargs.get('dosage_key')
        if kwargs.get('address', None) is not None:
            institution.address = kwargs.get('address')
        if kwargs.get('phone', None) is not None:
            institution.phone = kwargs.get('phone')
        if kwargs.get('type', None) is not None:
            institution.type = kwargs.get('type')

        institution.save()

        return UpdateInstitution(institution=institution)


class DeleteInstitution(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    status = graphene.String()

    @permission_required(['users.delete_institution'])
    def mutate(self, info, **kwargs):
        institution = Institution.objects.get(id=kwargs.get('id'))
        institution.delete()
        return DeleteInstitution(status="OK")


class CreateMedical(graphene.Mutation):
    medical = graphene.Field(lambda: MedicalType)

    class Arguments:
        institution_id = graphene.Int(required=True)
        first_name = graphene.String(required=True)
        middle_name = graphene.String()
        last_name = graphene.String()

    @permission_required(['users.add_medical'])
    def mutate(self, info, institution_id, first_name, **kwargs):
        medical = Medical(institution_id=institution_id, first_name=first_name)

        if kwargs.get('middle_name', None) is not None:
            medical.middle_name = kwargs.get('middle_name')
        if kwargs.get('last_name', None) is not None:
            medical.last_name = kwargs.get('last_name')

        medical.save()

        return CreateMedical(medical=medical)


class UpdateMedical(graphene.Mutation):
    medical = graphene.Field(lambda: MedicalType)

    class Arguments:
        id = graphene.Int(required=True)
        institution_id = graphene.Int()
        first_name = graphene.String()
        middle_name = graphene.String()
        last_name = graphene.String()

    @permission_required(['users.change_medical'])
    def mutate(self, info, id, **kwargs):
        medical = Medical.objects.filter(id=id).first()

        if not medical:
            raise ValueError("Medical not exists.")

        if kwargs.get('institution_id', None) is not None:
            medical.institution_id = kwargs.get('institution_id')
        if kwargs.get('first_name', None) is not None:
            medical.first_name = kwargs.get('first_name')
        if kwargs.get('middle_name', None) is not None:
            medical.middle_name = kwargs.get('middle_name')
        if kwargs.get('last_name', None) is not None:
            medical.last_name = kwargs.get('last_name')

        medical.save()

        return UpdateMedical(medical=medical)


class CreateEmployee(graphene.Mutation):
    employee = graphene.Field(lambda: EmployeeType)

    class Arguments:
        institution_id = graphene.Int(required=True)
        ci = graphene.Int(required=True)
        first_name = graphene.String(required=True)
        middle_name = graphene.String()
        last_name = graphene.String()
        gender = graphene.String(required=True)
        home_address = graphene.String()
        mobile_phone = graphene.Int()
        code_licence = graphene.String()

    @permission_required(['users.add_employee'])
    def mutate(self, info, institution_id, ci, first_name, gender, **kwargs):
        employee = Employee(institution_id=institution_id, ci=ci, first_name=first_name, gender=gender)

        if kwargs.get('middle_name', None) is not None:
            employee.middle_name = kwargs.get('middle_name')
        if kwargs.get('last_name', None) is not None:
            employee.last_name = kwargs.get('last_name')
        if kwargs.get('home_address', None) is not None:
            employee.home_address = kwargs.get('home_address')
        if kwargs.get('mobile_phone', None) is not None:
            employee.mobile_phone = kwargs.get('mobile_phone')
        if kwargs.get('code_licence', None) is not None:
            employee.code_licence = kwargs.get('code_licence')

        employee.save()

        return CreateEmployee(employee=employee)


class UpdateEmployee(graphene.Mutation):
    employee = graphene.Field(lambda: EmployeeType)

    class Arguments:
        id = graphene.Int(required=True)
        institution_id = graphene.Int()
        ci = graphene.Int()
        first_name = graphene.String()
        middle_name = graphene.String()
        last_name = graphene.String()
        gender = graphene.String()
        home_address = graphene.String()
        mobile_phone = graphene.Int()
        code_licence = graphene.String()

    @permission_required(['users.change_employee'])
    def mutate(self, info, id, **kwargs):
        employee = Employee.objects.filter(id=id).first()

        if not employee:
            raise ValueError("Employee not exists.")

        if kwargs.get('institution_id', None) is not None:
            employee.institution_id = kwargs.get('institution_id')
        if kwargs.get('ci', None) is not None:
            employee.ci = kwargs.get('ci')
        if kwargs.get('first_name', None) is not None:
            employee.first_name = kwargs.get('first_name')
        if kwargs.get('middle_name', None) is not None:
            employee.middle_name = kwargs.get('middle_name')
        if kwargs.get('last_name', None) is not None:
            employee.last_name = kwargs.get('last_name')
        if kwargs.get('gender', None) is not None:
            employee.gender = kwargs.get('gender')
        if kwargs.get('home_address', None) is not None:
            employee.home_address = kwargs.get('home_address')
        if kwargs.get('mobile_phone', None) is not None:
            employee.mobile_phone = kwargs.get('mobile_phone')
        if kwargs.get('code_licence', None) is not None:
            employee.code_licence = kwargs.get('code_licence')

        employee.save()

        return UpdateEmployee(employee=employee)


class CreateUser(graphene.Mutation):
    user = graphene.Field(lambda: UserType)

    class Arguments:
        profile_id = graphene.Int(required=True)
        group_ids = graphene.List(graphene.Int, required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    @permission_required(['users.add_user'])
    def mutate(self, info, profile_id, group_ids, username, password, **kwargs):
        profile = Employee.objects.get(id=profile_id)

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        profile.user = user
        profile.save()

        for g in group_ids:
            group = Group.objects.get(pk=g)
            user.groups.add(group)

        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    user = graphene.Field(lambda: UserType)

    class Arguments:
        id = graphene.Int(required=True)
        is_active = graphene.Boolean()
        group_ids = graphene.List(graphene.Int)
        password = graphene.String()

    @permission_required(['users.change_user'])
    def mutate(self, info, id, **kwargs):
        user = User.objects.filter(id=id).first()

        if not user:
            raise ValueError("User not exists.")

        if kwargs.get('is_active', None) is not None:
            user.is_active = kwargs.get('is_active')

        user.save()

        return UpdateUser(user=user)


class CreatePatient(graphene.Mutation):
    patient = graphene.Field(lambda: PatientType)

    class Arguments:
        first_name = graphene.String(required=True)
        middle_name = graphene.String(required=True)
        last_name = graphene.String()
        phone = graphene.Int()
        institution_id = graphene.Int()
        ci = graphene.String()
        is_real_birthdate = graphene.Boolean(required=True)
        birth_date = graphene.Date()
        gender = graphene.String()

    @permission_required(['users.add_patient'])
    def mutate(self, info, first_name, middle_name,is_real_birthdate, **kwargs):
        patient = Patient(first_name=first_name, middle_name=middle_name, is_real_birthdate=is_real_birthdate)
        if kwargs.get('last_name', None) is not None:
            patient.last_name = kwargs.get('last_name')
        if kwargs.get('phone', None) is not None:
            patient.phone = kwargs.get('phone')
        if kwargs.get('institution_id', None) is not None:
            patient.institution_id = kwargs.get('institution_id')
        if kwargs.get('ci', None) is not None:
            patient.ci = kwargs.get('ci')
        if kwargs.get('birth_date', None) is not None:
            patient.birth_date = kwargs.get('birth_date')
        if kwargs.get('gender', None) is not None:
            patient.gender = kwargs.get('gender')
        patient.save()

        return CreatePatient(patient=patient)


class UpdatePatient(graphene.Mutation):
    patient = graphene.Field(lambda: PatientType)

    class Arguments:
        id = graphene.Int(required=True)
        first_name = graphene.String()
        middle_name = graphene.String()
        last_name = graphene.String()
        phone = graphene.Int()
        institution_id = graphene.Int()
        ci = graphene.String()
        is_real_birthdate = graphene.Boolean()
        birth_date = graphene.Date()
        gender = graphene.String()

    @permission_required(['users.change_patient'])
    def mutate(self, info, id, **kwargs):
        patient = Patient.objects.filter(id=id).first()

        if not patient:
            raise ValueError("Patient not exists.")

        if kwargs.get('first_name', None) is not None:
            patient.first_name = kwargs.get('first_name')
        if kwargs.get('middle_name', None) is not None:
            patient.middle_name = kwargs.get('middle_name')
        if kwargs.get('last_name', None) is not None:
            patient.last_name = kwargs.get('last_name')
        if kwargs.get('phone', None) is not None:
            patient.phone = kwargs.get('phone')
        if kwargs.get('institution_id', None) is not None:
            patient.institution_id = kwargs.get('institution_id')
        if kwargs.get('ci', None) is not None:
            patient.ci = kwargs.get('ci')
        if kwargs.get('birth_date', None) is not None:
            patient.birth_date = kwargs.get('birth_date')
        if kwargs.get('is_real_birthdate', None) is not None:
            patient.is_real_birthdate = kwargs.get('is_real_birthdate')
        if kwargs.get('gender', None) is not None:
            patient.gender = kwargs.get('gender')

        patient.save()

        return UpdatePatient(patient=patient)


class Mutation(graphene.ObjectType):
    create_institution = CreateInstitution.Field()
    update_institution = UpdateInstitution.Field()

    create_medical = CreateMedical.Field()
    update_medical = UpdateMedical.Field()

    create_employee = CreateEmployee.Field()
    update_employee = UpdateEmployee.Field()

    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()

    create_patient = CreatePatient.Field()
    update_patient = UpdatePatient.Field()
