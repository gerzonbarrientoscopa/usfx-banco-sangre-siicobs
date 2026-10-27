from __future__ import unicode_literals
import datetime
import graphene
from graphql_jwt.decorators import permission_required

from donors.models import Donor
from donations.models import Donation, Exam, PhysicalAnalysis, Rejected
from donations.schema import DonationType, ExamType, PhysicalAnalysisType, RejectedType
from users.templatetags.utils import calculate_age


class CreateDonation(graphene.Mutation):
    donation = graphene.Field(lambda: DonationType)

    class Arguments:
        donor_id = graphene.Int(required=True)
        type_donation = graphene.String(required=True)
        type_process = graphene.String(required=True)
        last_donation_at = graphene.Date()
        place_id = graphene.Int(required=True)
        event_id = graphene.Int()
        patient_id = graphene.Int()
        register_id = graphene.Int(required=True)
        employee_id = graphene.Int(required=True)
        register_at = graphene.Date(required=True)

    @permission_required(['donations.add_donation'])
    def mutate(self, info, donor_id, type_process, type_donation, place_id, register_at, register_id, employee_id,
               **kwargs):
        is_admin = False
        user = info.context.user

        if user.username == "admin":
            is_admin = True

        donor = Donor.objects.get(id=donor_id)
        age = 0
        if donor.birth_date:
            age = calculate_age(donor.birth_date)

        donation = Donation(donor_id=donor_id, age_donor=age, register_at=register_at, place_id=place_id,
                            type_process=type_process, type_donation=type_donation, employee_id=employee_id,
                            register_id=register_id)

        if kwargs.get('event_id', None) is not None:
            donation.event_id = kwargs.get('event_id')
        if kwargs.get('patient_id', None) is not None:
            donation.patient_id = kwargs.get('patient_id')
        if kwargs.get('last_donation_at', None) is not None:
            donation.last_donation_at = kwargs.get('last_donation_at')

        donor = Donor.objects.get(id=donor_id)

        if donor.birth_date is None:
            raise ValueError('donor: Actualiza los datos del donante antes de proseguir')

        if not is_admin and Donation.objects.filter(donor=donor, register_at=register_at).exists():
            raise ValueError('donor: No tienes permiso para registrar duplicados, por favor consulte a dirección')

        donation.save()

        Exam.objects.create(donation_id=donation.id, employee_id=donation.employee.id, register_at=donation.register_at,
                            register_id=donation.register.id)
        PhysicalAnalysis.objects.create(donation_id=donation.id, employee_id=donation.employee.id,
                                        register_at=donation.register_at, register_id=donation.register.id)

        return CreateDonation(donation=donation)


class UpdateDonation(graphene.Mutation):
    donation = graphene.Field(lambda: DonationType)

    class Arguments:
        id = graphene.Int(required=True)
        donor_id = graphene.Int()
        type_donation = graphene.String()
        type_process = graphene.String()
        last_donation_at = graphene.Date()
        place_id = graphene.Int()
        event_id = graphene.Int()
        patient_id = graphene.Int()
        register_id = graphene.Int()
        employee_id = graphene.Int()
        register_at = graphene.Date()

    @permission_required(['donations.change_donation'])
    def mutate(self, info, id, **kwargs):
        donation = Donation.objects.filter(id=id).first()

        if donation is None:
            raise ValueError("Donation not exists.")

        donation.event_id = kwargs.get('event_id')
        if kwargs.get('donor_id', None) is not None:
            donation.donor_id = kwargs.get('donor_id')
        if kwargs.get('type_process', None) is not None:
            donation.type_process = kwargs.get('type_process')
        if kwargs.get('type_donation', None) is not None:
            donation.type_donation = kwargs.get('type_donation')
        if kwargs.get('last_donation_at', None) is not None:
            donation.last_donation_at = kwargs.get('last_donation_at')
        if kwargs.get('place_id', None) is not None:
            donation.place_id = kwargs.get('place_id')
        if kwargs.get('patient_id', None) is not None:
            donation.patient_id = kwargs.get('patient_id')
        if kwargs.get('register_id', None) is not None:
            donation.register_id = kwargs.get('register_id')
        if kwargs.get('employee_id', None) is not None:
            donation.employee_id = kwargs.get('employee_id')
        if kwargs.get('register_at', None) is not None:
            donation.register_at = kwargs.get('register_at')

        donation.save()

        return UpdateDonation(donation=donation)


class CreateExam(graphene.Mutation):
    exam = graphene.Field(lambda: ExamType)

    class Arguments:
        donation_id = graphene.Int(required=True)
        hematocrit = graphene.Float()
        hemoglobin = graphene.Float()
        blood_group = graphene.String()
        chagas = graphene.String()
        rpr = graphene.String()
        employee_id = graphene.Int(required=True)
        register_id = graphene.Int(required=True)
        observations = graphene.String()
        register_at = graphene.Date(required=True)

    @permission_required(['donations.add_exam'])
    def mutate(self, info, donation_id, employee_id, register_id, register_at, **kwargs):
        _exam = Exam.objects.filter(donation_id=donation_id).first()

        if _exam is not None:
            raise ValueError('donation_id: debe ser unico')

        exam = Exam(donation_id=donation_id, employee_id=employee_id, register_id=register_id, register_at=register_at)

        if kwargs.get('hematocrit', None) is not None:
            exam.hematocrit = kwargs.get('hematocrit')
        if kwargs.get('hemoglobin', None) is not None:
            exam.hemoglobin = kwargs.get('hemoglobin')
        if kwargs.get('blood_group', None) is not None:
            exam.blood_group = kwargs.get('blood_group')
        if kwargs.get('rpr', None) is not None:
            exam.rpr = kwargs.get('rpr')
        if kwargs.get('chagas', None) is not None:
            exam.chagas = kwargs.get('chagas')
        if kwargs.get('employee_id', None) is not None:
            exam.employee_id = kwargs.get('employee_id')
        if kwargs.get('register_id', None) is not None:
            exam.register_id = kwargs.get('register_id')
        if kwargs.get('register_at', None) is not None:
            exam.register_at = kwargs.get('register_at')
        if kwargs.get('observations', None) is not None:
            exam.observations = kwargs.get('observations')

        exam.save()

        return CreateExam(exam=exam)


class UpdateExam(graphene.Mutation):
    exam = graphene.Field(lambda: ExamType)

    class Arguments:
        id = graphene.Int(required=True)
        donation_id = graphene.Int()
        hematocrit = graphene.Float()
        hemoglobin = graphene.Float()
        blood_group = graphene.String()
        chagas = graphene.String()
        rpr = graphene.String()
        employee_id = graphene.Int()
        register_id = graphene.Int()
        observations = graphene.String()
        register_at = graphene.Date()

    @permission_required(['donations.change_exam'])
    def mutate(self, info, id, **kwargs):
        exam = Exam.objects.filter(id=id).first()
        if not exam:
            raise ValueError("Exam not exists.")

        if kwargs.get('donation_id', None) is not None:
            exam.donation_id = kwargs.get('donation_id')
        if kwargs.get('hematocrit', None) is not None:
            exam.hematocrit = kwargs.get('hematocrit')
        if kwargs.get('hemoglobin', None) is not None:
            exam.hemoglobin = kwargs.get('hemoglobin')
        if kwargs.get('blood_group', None) is not None:
            exam.blood_group = kwargs.get('blood_group')
        if kwargs.get('rpr', None) is not None:
            exam.rpr = kwargs.get('rpr')
        if kwargs.get('chagas', None) is not None:
            exam.chagas = kwargs.get('chagas')
        if kwargs.get('employee_id', None) is not None:
            exam.employee_id = kwargs.get('employee_id')
        if kwargs.get('register_id', None) is not None:
            exam.register_id = kwargs.get('register_id')
        if kwargs.get('observations', None) is not None:
            exam.observations = kwargs.get('observations')
        if kwargs.get('register_at', None) is not None:
            exam.register_at = kwargs.get('register_at')

        exam.save()

        return UpdateExam(exam=exam)


class CreatePhysicalAnalysis(graphene.Mutation):
    physicalanalysis = graphene.Field(lambda: PhysicalAnalysisType)

    class Arguments:
        donation_id = graphene.Int(required=True)
        systolic = graphene.Float()
        diastolic = graphene.Float()
        pulse = graphene.Float()
        tall = graphene.Float()
        weight = graphene.Float()
        temperature = graphene.Float()
        employee_id = graphene.Int(required=True)
        register_id = graphene.Int(required=True)
        observations = graphene.String()
        register_at = graphene.Date(required=True)

    @permission_required(['donations.add_physicalanalysis'])
    def mutate(self, info, donation_id, employee_id, register_id, register_at, **kwargs):
        _physicalanalysis = PhysicalAnalysis.objects.filter(donation_id=donation_id).first()

        if _physicalanalysis is not None:
            raise ValueError('donation_id: debe ser unico')

        physicalanalysis = PhysicalAnalysis(donation_id=donation_id, employee_id=employee_id, register_id=register_id,
                                            register_at=register_at)
        if kwargs.get('systolic', None) is not None:
            physicalanalysis.systolic = kwargs.get('systolic')
        if kwargs.get('diastolic', None) is not None:
            physicalanalysis.diastolic = kwargs.get('diastolic')
        if kwargs.get('pulse', None) is not None:
            physicalanalysis.pulse = kwargs.get('pulse')
        if kwargs.get('weight', None) is not None:
            physicalanalysis.weight = kwargs.get('weight')
        if kwargs.get('tall', None) is not None:
            physicalanalysis.tall = kwargs.get('tall')
        if kwargs.get('temperature', None) is not None:
            physicalanalysis.temperature = kwargs.get('temperature')
        if kwargs.get('observations', None) is not None:
            physicalanalysis.observations = kwargs.get('observations')

        physicalanalysis.save()

        return CreatePhysicalAnalysis(physicalanalysis=physicalanalysis)


class UpdatePhysicalAnalysis(graphene.Mutation):
    physicalanalysis = graphene.Field(lambda: PhysicalAnalysisType)

    class Arguments:
        id = graphene.Int(required=True)
        donation_id = graphene.Int()
        systolic = graphene.Float()
        diastolic = graphene.Float()
        pulse = graphene.Float()
        tall = graphene.Float()
        weight = graphene.Float()
        temperature = graphene.Float()
        employee_id = graphene.Int()
        register_id = graphene.Int()
        observations = graphene.String()
        register_at = graphene.Date()

    @permission_required(['donations.change_physicalanalysis'])
    def mutate(self, info, id, **kwargs):
        physicalanalysis = PhysicalAnalysis.objects.filter(id=id).first()
        if not physicalanalysis:
            raise ValueError("PhysicalAnalysis not exists.")

        if kwargs.get('donation_id', None) is not None:
            physicalanalysis.donation_id = kwargs.get('donation_id')
        if kwargs.get('systolic', None) is not None:
            physicalanalysis.systolic = kwargs.get('systolic')
        if kwargs.get('diastolic', None) is not None:
            physicalanalysis.diastolic = kwargs.get('diastolic')
        if kwargs.get('pulse', None) is not None:
            physicalanalysis.pulse = kwargs.get('pulse')
        if kwargs.get('weight', None) is not None:
            physicalanalysis.weight = kwargs.get('weight')
        if kwargs.get('tall', None) is not None:
            physicalanalysis.tall = kwargs.get('tall')
        if kwargs.get('temperature', None) is not None:
            physicalanalysis.temperature = kwargs.get('temperature')
        if kwargs.get('employee_id', None) is not None:
            physicalanalysis.employee_id = kwargs.get('employee_id')
        if kwargs.get('register_id', None) is not None:
            physicalanalysis.register_id = kwargs.get('register_id')
        if kwargs.get('observations', None) is not None:
            physicalanalysis.observations = kwargs.get('observations')
        if kwargs.get('register_at', None) is not None:
            physicalanalysis.register_at = kwargs.get('register_at')

        physicalanalysis.save()

        return UpdatePhysicalAnalysis(physicalanalysis=physicalanalysis)


def update_donor(rejected):
    if rejected.reason.type == 'PE':
        donor = Donor.objects.get(id=rejected.donation.donor.id)

        if donor and donor.can_donate:
            donor.can_donate = False
            donor.save()


class CreateRejected(graphene.Mutation):
    rejected = graphene.Field(RejectedType)

    class Arguments:
        donation_id = graphene.Int(required=True)
        reason_id = graphene.Int(required=True)
        employee_id = graphene.Int(required=True)
        resource_id = graphene.Int(required=True)
        resource = graphene.String(required=True)
        observations = graphene.String()
        register_at = graphene.Date(required=True)

    @permission_required(['donations.add_rejected'])
    def mutate(self, info, reason_id, donation_id, employee_id, resource, resource_id, register_at, **kwargs):
        rejected = Rejected(reason_id=reason_id, donation_id=donation_id, employee_id=employee_id,
                            resource_id=resource_id, resource=resource, register_at=register_at)

        if kwargs.get('observations', None) is not None:
            rejected.observations = kwargs.get('observations')

        rejected.save()
        update_donor(rejected)

        return CreateRejected(rejected=rejected)


class UpdateRejected(graphene.Mutation):
    rejected = graphene.Field(RejectedType)

    class Arguments:
        id = graphene.Int(required=True)
        donation_id = graphene.Int()
        reason_id = graphene.Int()
        employee_id = graphene.Int()
        resource_id = graphene.Int()
        resource = graphene.String()
        observations = graphene.String()
        register_at = graphene.Date()

    @permission_required(['donations.change_rejected'])
    def mutate(self, info, id, **kwargs):
        rejected = Rejected.objects.filter(id=id).first()
        if rejected is None:
            raise ValueError('Rejected not found')

        if kwargs.get('reason_id', None) is not None:
            rejected.reason_id = kwargs.get('reason_id')
        if kwargs.get('donation_id', None) is not None:
            rejected.donation_id = kwargs.get('donation_id')
        if kwargs.get('employee_id', None) is not None:
            rejected.employee_id = kwargs.get('employee_id')
        if kwargs.get('resource', None) is not None:
            rejected.resource = kwargs.get('resource')
        if kwargs.get('resource_id', None) is not None:
            rejected.resource_id = kwargs.get('resource_id')
        if kwargs.get('register_at', None) is not None:
            rejected.register_at = kwargs.get('register_at')
        if kwargs.get('observations', None) is not None:
            rejected.observations = kwargs.get('observations')

        rejected.save()
        update_donor(rejected)

        return UpdateRejected(rejected=rejected)


class DeleteRejected(graphene.Mutation):
    rejected = graphene.Field(RejectedType)

    class Arguments:
        id = graphene.Int(required=True)

    @permission_required(['donations.delete_rejected'])
    def mutate(self, info, id, **kwargs):
        rejected = Rejected.objects.get(id=id)
        rejected.delete()

        return DeleteRejected(rejected=rejected)


class Mutation(graphene.ObjectType):
    create_donation = CreateDonation.Field()
    update_donation = UpdateDonation.Field()

    create_exam = CreateExam.Field()
    update_exam = UpdateExam.Field()

    create_physicalanalysis = CreatePhysicalAnalysis.Field()
    update_physicalanalysis = UpdatePhysicalAnalysis.Field()

    create_rejected = CreateRejected.Field()
    update_rejected = UpdateRejected.Field()
    delete_rejected = DeleteRejected.Field()
