# encoding:utf-8
from django.utils.safestring import mark_safe
from num2words import num2words

from django import template

from distributions.models import DistributionItemFragmentation
from donations.models import Exam, Rejected, PhysicalAnalysis, TYPE_DONATION, TYPE_CHAGAS, Donation
from donors.models import CIVIL_STATUS, DEGREE_INSTRUCTION, DEPARTMENTS
from extractions.models import ARM, Extraction, EVOLUTION, DETECTION, EXTRACTION_PLACE
from fragmentations.models import Release, Discard, ItemFragmentation
from laboratories.models import Immunohematology, TYPE_REACT
from packages.models import Package
from settings.models import TYPE_REASON
from siicobs_main.utils_global import get_age_from_birthday
from users.models import GENDER, TYPE_INSTITUTION
from datetime import date

register = template.Library()


@register.simple_tag
def clean_value(value, suffix=''):
    if value is None:
        return ''
    return str(value).replace('.', ',') + ' ' + suffix


@register.filter
def isNone(value):
    if value is None:
        return ''
    return value


@register.filter
def cleanValue(value):
    if value is None or value == 'null':
        return ''
    return value


@register.filter
def cleanValueNumber(value):
    if value is None:
        return 0
    return value


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    return instance._meta.get_field(field_name).verbose_name


@register.simple_tag
def build_spaces(tag, quantity):
    new_string = str(tag) * quantity
    return new_string


@register.simple_tag
def get_field_name(obj, field_name):
    return obj._meta.get_field(field_name).verbose_name.title()


@register.filter()
def to_int(value):
    return int(value)


@register.simple_tag
def get_bloodBag(x):
    if x:
        a = x[len(x) - 1]
        if a == '+':
            b = x.split('+')
        else:
            b = x.split('-')
        return str(b[0]) + ' RH ' + str(a)
    else:
        return ''


@register.simple_tag
def get_factor_rh_literal(x):
    if x:
        a = x[len(x) - 1]
        if a == '+':
            b = x.split('+')
            l = ' Positivo (+)'
        else:
            b = x.split('-')
            l = ' Negativo (-)'

        return str(b[0]) + l
    else:
        return ''


@register.filter
def fullInitialName(profile):
    initials = ''
    if profile.first_name:
        initials += profile.first_name[0] + '.'
    if profile.middle_name:
        initials += profile.middle_name[0] + '.'
    if profile.last_name:
        initials += profile.last_name[0] + '.'

    return initials


@register.filter
def full_name(profile):
    initials = ''
    if profile.first_name:
        initials += profile.first_name + ' '
    if profile.middle_name:
        initials += profile.middle_name + ' '
    if profile.last_name:
        initials += profile.last_name

    return initials


@register.filter
def full_initials_employee(profile):
    initials = ''
    if profile:
        if profile.first_name:
            initials += profile.first_name[0]
        if profile.middle_name:
            initials += profile.middle_name[0]
        if profile.last_name:
            initials += profile.last_name[0]

    return initials


@register.simple_tag
def get_statusExam(id):
    filtered = Exam.objects.filter(donation=id)
    if filtered:
        return 'SI'
    else:
        return 'NO'


@register.simple_tag
def get_statusPhysicalAnalysis(id):
    filtered = PhysicalAnalysis.objects.filter(donation=id)
    if filtered:
        return 'SI'
    else:
        return 'NO'


@register.simple_tag
def get_statusExtraction(id):
    filtered = Extraction.objects.filter(donation=id)
    if filtered:
        return 'SI'
    else:
        return 'NO'


@register.simple_tag
def get_statusRejected(id):
    filtered = Rejected.objects.filter(donation=id)
    if filtered:
        return 'SI'
    else:
        return 'NO'


@register.simple_tag
def get_statusImmunoserology(data):
    if data == 'flag':
        return 'NO'
    elif data.hiv == 'R' or data.hbsag == 'R' or data.hvc == 'R' or data.cheia == 'R' or data.chagas_hai == 'R' or data.rpr == 'R':
        return 'SI'
    else:
        return 'NO'


@register.simple_tag
def get_exam_hematocrit(id):
    query = Exam.objects.filter(donation=id).first()
    if query:
        return query.hematocrit
    else:
        return ''


@register.simple_tag
def get_exam_hemoglobin(id):
    query = Exam.objects.filter(donation=id).first()
    if query:
        return query.hemoglobin
    else:
        return ''


@register.simple_tag
def get_gender_user(gender):
    for status in GENDER:
        if status[0] == gender:
            return status[1]
    return None


@register.simple_tag
def get_type_arm(arm):
    for status in ARM:
        if status[0] == arm:
            return status[1]
    return None


@register.simple_tag
def get_reason_type(type):
    for status in TYPE_REASON:
        if status[0] == type:
            return status[1]
    return None


@register.simple_tag
def calculate_age(born, today=date.today()):
    age = get_age_from_birthday(born, today)
    return age


@register.simple_tag
def get_civil_status(value):
    for status in CIVIL_STATUS:
        if status[0] == value:
            return status[1]
    return None


@register.simple_tag
def get_degree(value):
    for status in DEGREE_INSTRUCTION:
        if status[0] == value:
            return status[1]
    return None


@register.simple_tag
def get_department(value):
    for status in DEPARTMENTS:
        if status[0] == value:
            return status[1]
    return None


@register.simple_tag
def get_evolution(value):
    for status in EVOLUTION:
        if status[0] == value:
            return status[1]
    return None


@register.simple_tag
def get_detection(value):
    for status in DETECTION:
        if status[0] == value:
            return status[1]
    return None


@register.simple_tag
def get_extraction_place(value):
    for status in EXTRACTION_PLACE:
        if status[0] == value:
            return status[1]
    return ''


@register.simple_tag
def get_type_donation(value):
    for status in TYPE_DONATION:
        if status[0] == value:
            return status[1]
    return ''


@register.simple_tag
def get_type_chagas_or_rpr(value):
    for status in TYPE_CHAGAS:
        if status[0] == value:
            return status[1]
    return ''


@register.simple_tag
def get_abc(value):
    a = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    return a[value]


@register.simple_tag
def literal_price_entero(price):
    literal_amount = num2words(int(price), lang='es')
    return str(literal_amount).upper()


@register.simple_tag
def decimal_amount(price):
    decimal_amount = get_decimal_amount(price)
    return decimal_amount


def get_decimal_amount(price):
    total_str = str(price)
    array_split = total_str.split('.')
    residue = '00'
    if len(array_split) != 1:
        residue = array_split[1]
    if len(residue) == 1:
        residue += '0'
    return residue


@register.simple_tag
def get_fenotype(fenotype):
    if fenotype == '-':
        return '-'
    else:
        return '+'


@register.simple_tag
def get_message_antikell(immunohematology):
    message_antikell = ''
    if immunohematology and immunohematology.antikell != '-':
        message_antikell = '<b>Transfundir a personas de la tercera edad.</b>'
    return message_antikell


@register.simple_tag
def get_message_type_irregular_antibody(itemfragmentation):
    message = ''
    if itemfragmentation and itemfragmentation.type_irregular_antibody:
        message = itemfragmentation.type_irregular_antibody.text_bag
    return message


@register.simple_tag
def get_blood_group_from_extraction(extraction_id):
    donation = Donation.objects.filter(extraction__id=extraction_id).first()
    exists_immunohematology = Immunohematology.objects.filter(donation_id=donation.id).exists()
    if donation and exists_immunohematology:
        return get_blood_group(donation.immunohematology)
    return ''


@register.simple_tag
def get_blood_group(immunohematology):
    blood_group = immunohematology.direct_abo
    if blood_group:
        if blood_group == 'A1':
            blood_group = 'A<sub>1</sub>'
        elif blood_group == 'A2':
            blood_group = 'A<sub>2</sub>'
        elif blood_group == 'A1B':
            blood_group = 'A<sub>1</sub>B'
        elif blood_group == 'A2B':
            blood_group = 'A<sub>2</sub>B'
    return mark_safe(blood_group)


@register.simple_tag
def get_factor_rh_from_extraction(extraction_id):
    donation = Donation.objects.filter(extraction__id=extraction_id).first()
    exists_immunohematology = Immunohematology.objects.filter(donation_id=donation.id).exists()

    if donation and exists_immunohematology:
        return get_factor_rh(donation.immunohematology)
    return ''


@register.simple_tag
def get_factor_rh(immunohematology):
    factor_rh = immunohematology.factor_rh
    factor_rh_text = ''
    if factor_rh:
        if factor_rh == 'RH-':
            factor_rh_text = 'Rh D NEGATIVO'
        elif factor_rh == 'RH+':
            factor_rh_text = 'Rh D POSITIVO'
        else:
            factor_rh_text = 'Rh D POSITIVO <br> Du Débil'
    return factor_rh_text


@register.simple_tag
def get_itemfragmentations(distribution_id):
    return DistributionItemFragmentation.objects.filter(distribution_id=distribution_id)


@register.simple_tag
def get_hemocomponent_from_fragmentation(fragmentation_id, hemocomponent_id):
    items = ItemFragmentation.objects.filter(fragmentation_id=fragmentation_id, typehemocomponent_id=hemocomponent_id)
    if items:
        return 'X'
    return ''


@register.simple_tag
def get_itemfragmentations_price(distribution_id):
    difs = DistributionItemFragmentation.objects.filter(distribution_id=distribution_id)
    total = 00.00
    for dif in difs:
        package = Package.objects.filter(typehemocomponent_id=dif.itemfragmentation.typehemocomponent.id).first()
        if package:
            total = total + float(package.price)
    return total


@register.simple_tag
def get_discard_for_item(item):
    return Discard.objects.filter(itemfragmentation_id=item.id).first()


@register.simple_tag
def get_release_for_item(item):
    return Release.objects.filter(itemfragmentation_id=item.id).first()


@register.simple_tag
def get_distribution_for_item(item):
    return DistributionItemFragmentation.objects.filter(itemfragmentation_id=item.id).first()


@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    return float(qty * unit_price)


@register.simple_tag()
def get_dashed_line(quantity):
    return '-' * quantity


@register.simple_tag
def get_react_type(type):
    for status in TYPE_REACT:
        if status[0] == type:
            return status[1]
    return None

@register.filter
def get_institution_type(type):
    for status in TYPE_INSTITUTION:
        if status[0] == type:
            return status[1]
    return None
