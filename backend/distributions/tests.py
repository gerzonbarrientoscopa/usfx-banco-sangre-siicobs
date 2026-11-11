import datetime

from django.test import TestCase
from django.utils import timezone

from distributions.age_groups import filter_by_age_group
from distributions.models import Distribution
from users.models import Employee, Institution, Medical, Patient


class DistributionAgeGroupFilterTests(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(name='Institución de prueba')
        self.employee = Employee.objects.create(
            institution=self.institution,
            ci=990001,
            first_name='Empleado',
            gender='M',
        )
        self.medical = Medical.objects.create(
            institution=self.institution,
            first_name='Médico',
        )
        self.patient = Patient.objects.create(
            institution=self.institution,
            ci='990001',
            gender='M',
            birth_date=datetime.date(2000, 1, 1),
        )
        self.register_at = timezone.now()

    def create_distribution(self, age, age_type):
        distribution = Distribution.objects.create(
            institution=self.institution,
            employee=self.employee,
            medical=self.medical,
            patient=self.patient,
            register_at=self.register_at,
        )
        Distribution.objects.filter(pk=distribution.pk).update(
            age_patient=age,
            age_patient_type=age_type,
        )
        return distribution

    def test_age_groups_filter_by_saved_age_and_unit(self):
        neonatal = self.create_distribution(28, 'D')
        under_one_day_based = self.create_distribution(29, 'D')
        under_one_month_based = self.create_distribution(11, 'M')
        under_one_year_legacy = self.create_distribution(0, 'Y')
        groups = [
            ('AGE_1_4', 1, 4),
            ('AGE_5_9', 5, 9),
            ('AGE_10_19', 10, 19),
            ('AGE_20_34', 20, 34),
            ('AGE_35_49', 35, 49),
            ('AGE_50_64', 50, 64),
            ('AGE_OVER_64', 65, 65),
        ]
        expected_ids = {
            'NEONATE': [neonatal.id],
            'UNDER_1': [
                under_one_day_based.id,
                under_one_month_based.id,
                under_one_year_legacy.id,
            ],
        }

        for group, minimum, maximum in groups:
            distribution = self.create_distribution(minimum, 'Y')
            if maximum != minimum:
                self.create_distribution(maximum, 'Y')
            expected_ids[group] = list(
                Distribution.objects.filter(
                    age_patient_type='Y',
                    age_patient__gte=minimum,
                    age_patient__lte=maximum,
                ).values_list('id', flat=True)
            )

        for group, distribution_ids in expected_ids.items():
            self.assertCountEqual(
                filter_by_age_group(Distribution.objects.all(), group).values_list('id', flat=True),
                distribution_ids,
            )

    def test_new_distribution_saves_age_in_days_for_neonates(self):
        register_at = timezone.now().replace(hour=12, minute=0, second=0, microsecond=0)
        patient = Patient.objects.create(
            institution=self.institution,
            ci='990002',
            gender='M',
            birth_date=register_at.date() - datetime.timedelta(days=28),
        )
        distribution = Distribution.objects.create(
            institution=self.institution,
            employee=self.employee,
            medical=self.medical,
            patient=patient,
            register_at=register_at,
        )

        self.assertEqual(distribution.age_patient, 28)
        self.assertEqual(distribution.age_patient_type, 'D')
