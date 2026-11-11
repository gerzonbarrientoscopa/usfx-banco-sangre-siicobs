from django.db import migrations, models
import django.core.validators
from django.db.models import Q


TYPE_BAG_BY_OLD_QUANTITY = {
    1: 'SIMPLE',
    2: 'DOBLE',
    3: 'TRIPLE',
    4: 'CUADRUPLE',
    5: 'CUADRUPLE_CON_FILTRO',
    6: 'SET_AFERESIS',
}


def migrate_type_bag(apps, schema_editor):
    Extraction = apps.get_model('extractions', 'Extraction')
    alias = schema_editor.connection.alias
    invalid_quantities = list(
        Extraction.objects.using(alias)
        .exclude(bags_quantity__in=TYPE_BAG_BY_OLD_QUANTITY.keys())
        .values_list('bags_quantity', flat=True)
        .distinct()
    )
    if invalid_quantities:
        raise RuntimeError(
            'Hay extracciones con bags_quantity fuera del rango esperado (1 a 6): '
            + ', '.join(str(value) for value in invalid_quantities)
        )

    for old_quantity, type_bag in TYPE_BAG_BY_OLD_QUANTITY.items():
        Extraction.objects.using(alias).filter(bags_quantity=old_quantity).update(
            type_bag=type_bag,
        )
    Extraction.objects.using(alias).filter(bags_quantity=5).update(bags_quantity=4)
    Extraction.objects.using(alias).filter(bags_quantity=6).update(bags_quantity=2)


def reverse_type_bag(apps, schema_editor):
    Extraction = apps.get_model('extractions', 'Extraction')
    alias = schema_editor.connection.alias
    Extraction.objects.using(alias).filter(type_bag='CUADRUPLE_CON_FILTRO').update(bags_quantity=5)
    Extraction.objects.using(alias).filter(type_bag='SET_AFERESIS').update(bags_quantity=6)


class Migration(migrations.Migration):

    dependencies = [
        ('extractions', '0004_extraction_typeanticoagulant'),
    ]

    operations = [
        migrations.AddField(
            model_name='extraction',
            name='type_bag',
            field=models.CharField(
                choices=[
                    ('SIMPLE', 'SIMPLE'),
                    ('DOBLE', 'DOBLE'),
                    ('TRIPLE', 'TRIPLE'),
                    ('CUADRUPLE', 'CUADRUPLE'),
                    ('CUADRUPLE_CON_FILTRO', 'CUADRUPLE CON FILTRO'),
                    ('SET_AFERESIS', 'SET DE AFERESIS'),
                ],
                default='SIMPLE',
                max_length=24,
                null=True,
                verbose_name='Tipo de bolsa',
            ),
        ),
        migrations.RunPython(migrate_type_bag, reverse_type_bag),
        migrations.AlterField(
            model_name='extraction',
            name='bags_quantity',
            field=models.SmallIntegerField(
                default=1,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(4),
                ],
                verbose_name='Cantidad de bolsas',
            ),
        ),
        migrations.AlterField(
            model_name='extraction',
            name='type_bag',
            field=models.CharField(
                choices=[
                    ('SIMPLE', 'SIMPLE'),
                    ('DOBLE', 'DOBLE'),
                    ('TRIPLE', 'TRIPLE'),
                    ('CUADRUPLE', 'CUADRUPLE'),
                    ('CUADRUPLE_CON_FILTRO', 'CUADRUPLE CON FILTRO'),
                    ('SET_AFERESIS', 'SET DE AFERESIS'),
                ],
                default='SIMPLE',
                max_length=24,
                verbose_name='Tipo de bolsa',
            ),
        ),
        migrations.AddConstraint(
            model_name='extraction',
            constraint=models.CheckConstraint(
                check=(
                    Q(type_bag='SIMPLE', bags_quantity=1) |
                    Q(type_bag='DOBLE', bags_quantity=2) |
                    Q(type_bag='TRIPLE', bags_quantity=3) |
                    Q(type_bag='CUADRUPLE', bags_quantity=4) |
                    Q(type_bag='CUADRUPLE_CON_FILTRO', bags_quantity=4) |
                    Q(type_bag='SET_AFERESIS', bags_quantity=2)
                ),
                name='extraction_type_bag_quantity_valid',
            ),
        ),
    ]
