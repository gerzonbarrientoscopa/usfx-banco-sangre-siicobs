from django.db import migrations, models


RESTRICTED_HEMOCOMPONENTS = {
    'plasma fresco congelado',
    'crioprecipitado',
    'concentrado de plaquetas',
}


def mark_restricted_hemocomponents(apps, schema_editor):
    TypeHemocomponent = apps.get_model('packages', 'TypeHemocomponent')
    restricted_ids = []

    for hemocomponent in TypeHemocomponent.objects.all().only('id', 'name'):
        normalized_name = ' '.join(hemocomponent.name.casefold().split())
        if normalized_name in RESTRICTED_HEMOCOMPONENTS:
            restricted_ids.append(hemocomponent.id)

    TypeHemocomponent.objects.filter(id__in=restricted_ids).update(
        blocks_release_with_irregular_antibodies=True
    )


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='typehemocomponent',
            name='blocks_release_with_irregular_antibodies',
            field=models.BooleanField(
                default=False,
                verbose_name='Bloquear liberación con anticuerpos irregulares positivos',
            ),
        ),
        migrations.RunPython(
            mark_restricted_hemocomponents,
            migrations.RunPython.noop,
        ),
    ]
