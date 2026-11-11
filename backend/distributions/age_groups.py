from django.db.models import Q


AGE_GROUP_FILTERS = {
    'NEONATE': Q(age_patient_type='D', age_patient__gte=0, age_patient__lte=28),
    'UNDER_1': (
        Q(age_patient_type='D', age_patient__gt=28) |
        Q(age_patient_type='M', age_patient__lt=12) |
        Q(age_patient_type='Y', age_patient=0)
    ),
    'AGE_1_4': Q(age_patient_type='Y', age_patient__gte=1, age_patient__lte=4),
    'AGE_5_9': Q(age_patient_type='Y', age_patient__gte=5, age_patient__lte=9),
    'AGE_10_19': Q(age_patient_type='Y', age_patient__gte=10, age_patient__lte=19),
    'AGE_20_34': Q(age_patient_type='Y', age_patient__gte=20, age_patient__lte=34),
    'AGE_35_49': Q(age_patient_type='Y', age_patient__gte=35, age_patient__lte=49),
    'AGE_50_64': Q(age_patient_type='Y', age_patient__gte=50, age_patient__lte=64),
    'AGE_OVER_64': Q(age_patient_type='Y', age_patient__gte=65),
}


def filter_by_age_group(queryset, age_group):
    if not age_group:
        return queryset

    age_filter = AGE_GROUP_FILTERS.get(age_group)
    if age_filter is None:
        return queryset.none()

    return queryset.filter(patient__isnull=False).filter(age_filter)
