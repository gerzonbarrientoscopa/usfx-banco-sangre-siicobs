from dateutil.relativedelta import relativedelta
from django.db import migrations


def recalculate_patient_age(apps, schema_editor):
    Distribution = apps.get_model('distributions', 'Distribution')
    alias = schema_editor.connection.alias
    queryset = Distribution.objects.using(alias).select_related('patient').filter(
        patient__birth_date__isnull=False
    )

    batch = []
    for distribution in queryset.iterator(chunk_size=1000):
        registered_date = distribution.register_at.date()
        birth_date = distribution.patient.birth_date
        if birth_date > registered_date:
            continue

        age = relativedelta(registered_date, birth_date)
        if age.years > 0:
            distribution.age_patient = age.years
            distribution.age_patient_type = 'Y'
        elif age.months > 0:
            distribution.age_patient = age.months
            distribution.age_patient_type = 'M'
        else:
            distribution.age_patient = age.days
            distribution.age_patient_type = 'D'

        batch.append(distribution)
        if len(batch) == 1000:
            Distribution.objects.using(alias).bulk_update(
                batch, ['age_patient', 'age_patient_type']
            )
            batch = []

    if batch:
        Distribution.objects.using(alias).bulk_update(
            batch, ['age_patient', 'age_patient_type']
        )


class Migration(migrations.Migration):
    dependencies = [
        ('distributions', '0002_distribution_age_patient_type'),
        ('users', '0002_remove_institution_is_public_institution_type_and_more'),
    ]

    operations = [
        migrations.RunPython(recalculate_patient_age, migrations.RunPython.noop),
    ]
