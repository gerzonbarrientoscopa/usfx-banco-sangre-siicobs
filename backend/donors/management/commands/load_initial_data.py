import datetime
import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q

from donors.models import Donor


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


class Command(BaseCommand):
    def handle(self, **options):
        fixtures_dir = os.path.join(settings.BASE_DIR, 'donors', 'fixtures')
        donors_file = os.path.join(fixtures_dir, 'donors.json')

        json_data = open(donors_file)
        donors = json.load(json_data)

        for i, elem in enumerate(donors):
            code = elem.get('code', None)
            ci = elem.get('ci', None)
            if ci != ' ':
                ci = None
            if ci != 'NO':
                ci = None
            print("I=" + str(i) + '-' + str(code))

            donor = Donor.objects.filter(code=code).first()
            if donor:
                donor_ci = Donor.objects.filter(ci=ci).exclude(code=donor.code).first()
            else:
                donor_ci = Donor.objects.filter(ci=ci).first()
            if ci is None:
                donor_ci = None

            if donor and donor_ci:
                if donor.code != donor_ci.code:
                    donor.code_other = donor.code_other + ',' + donor_ci

            if donor and donor_ci:
                print(
                    'DUPLICADOS-> ' + str(donor.code) + ':' + str(donor_ci) + '-' + str(donor.ci) + ':' + str(
                        donor_ci.ci))
                code_other = str(donor_ci.code_other)
                if code_other != '':
                    code_other = code_other + ',' + str(donor.code)

                donor_ci.code_other = code_other
                donor_ci.code_other = code_other.replace("None,", "")
                donor_ci.save()

            elif donor_ci:
                print(
                    'DUPLICADOS2-> ' + str(code) + ':' + str(donor_ci.code) + '-' + str(donor_ci) + ':' + str(
                        donor_ci.ci))
                code_other = str(donor_ci.code_other)
                if code_other != '':
                    code_other = code_other + ',' + str(code)

                donor_ci.code_other = code_other
                donor_ci.code_other = code_other.replace("None,", "")
                donor_ci.save()
            elif donor:
                pass
            else:
                # print("Donor not found")
                donor = Donor()
                if elem.get('code', None) is not None:
                    donor.code = elem.get('code')
                if elem.get('first_name', None) is not None:
                    donor.first_name = elem.get('first_name')
                if elem.get('middle_name', None) is not None:
                    donor.middle_name = elem.get('middle_name')
                if elem.get('last_name', None) is not None:
                    donor.last_name = elem.get('last_name')
                if elem.get('birth_date', None) is not None:
                    donor.birth_date = datetime.datetime.strptime(elem.get('birth_date')[0:10], '%Y-%m-%d').date()
                if elem.get('gender', None) is not None:
                    donor.gender = elem.get('gender')
                if elem.get('civil_status', None) is not None:
                    donor.civil_status = elem.get('civil_status')
                if elem.get('is_volunteer', None) is not None:
                    donor.is_volunteer = elem.get('is_volunteer')
                if elem.get('country', None) is not None:
                    donor.country = elem.get('country')
                if elem.get('residence', None) is not None:
                    donor.residence = elem.get('residence')
                if elem.get('zone', None) is not None:
                    donor.zone = elem.get('zone')
                if elem.get('province', None) is not None:
                    donor.province = elem.get('province')
                if elem.get('phone', None) is not None:
                    donor.phone = elem.get('phone')
                if elem.get('mobile_phone', None) is not None:
                    donor.mobile_phone = elem.get('mobile_phone')
                if elem.get('family_phone', None) is not None:
                    donor.family_phone = elem.get('family_phone')
                if elem.get('occupation', None) is not None:
                    donor.profession = elem.get('occupation')
                if elem.get('profession', None) is not None:
                    donor.degree_instruction = elem.get('profession')
                if elem.get('department', None) is not None:
                    donor.department = elem.get('department')
                if elem.get('job', None) is not None:
                    donor.job = elem.get('job')
                if elem.get('job_address', None) is not None:
                    donor.job_address = elem.get('job_address')
                if elem.get('email', None) is not None:
                    donor.email = elem.get('email')
                if elem.get('group_abo', None) is not None:
                    donor.group_abo = elem.get('group_abo')
                if elem.get('factor_rh', None) is not None:
                    donor.factor_rh = elem.get('factor_rh')
                if elem.get('ci', None) is not None:
                    ci = elem.get('ci')
                    if ci == '':
                        ci = None
                    donor.ci = ci
                if elem.get('ci_extencion', None) is not None:
                    ci_extension = elem.get('ci_extencion')
                    if ci_extension in ['LP', 'OR', 'PO', 'CO', 'CH', 'TA', 'PA', 'BE', 'SC'] and len(ci_extension) == 2:
                        donor.ci_extension = ci_extension
                    else:
                        donor.ci_extension = None
                verify_ci = None
                if ci is not None:
                    verify_ci = Donor.objects.filter(ci=donor.ci).first()

                if verify_ci:
                    print("DUPLICATE 3-> " + str(verify_ci) + ' _ ' + str(donor))
                    code_other = str(verify_ci.code_other)
                    if code_other != '':
                        code_other = code_other + ',' + str(code)

                    verify_ci.code_other = code_other
                    verify_ci.code_other = code_other.replace("None,", "")
                    verify_ci.save()
                else:
                    donor.save()
            # print(donor.id)
        print("Awesome. Your data is loaded!")
        json_data.close()
