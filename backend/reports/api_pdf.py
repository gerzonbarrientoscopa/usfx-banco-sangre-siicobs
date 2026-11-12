from django.shortcuts import render

from distributions.age_groups import filter_by_age_group
from distributions.models import Distribution, DistributionItemFragmentation
from fragmentations.models import ItemFragmentation, Release, Fragmentation, Discard
from laboratories.models import Immunoserology, Immunohematology
from packages.models import TypeHemocomponent
from sieves.models import ClinicalHistoryAnswer
from django.db.models import Q

from datetime import datetime
import json
from django.utils import timezone
from django.views.generic import View

from donations.models import Donation, PhysicalAnalysis, Exam, Rejected
from extractions.models import AdverseReaction, Extraction, SelfExclusion
from refreshments.models import ExtractionRefreshment
from siicobs_main.render import Render
from users.models import Employee
from users.templatetags.utils import get_hemocomponent_from_fragmentation, get_release_for_item, get_discard_for_item, \
    get_itemfragmentations


class GeneralPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()
        event = data['event']
        typeDonation = data['typeDonation']

        by_gender = [Donation.objects.filter(donor__gender='F', register_at__range=[date_init, date_end]).count(),
                     Donation.objects.filter(donor__gender='M', register_at__range=[date_init, date_end]).count(),
                     Donation.objects.filter(register_at__range=[date_init, date_end]).count()]

        by_event = [Donation.objects.filter(event__isnull=True, register_at__range=[date_init, date_end]).count(),
                    Donation.objects.filter(event__isnull=False, register_at__range=[date_init, date_end]).count(),
                    Donation.objects.filter(register_at__range=[date_init, date_end]).count()]

        by_typeDonation = [
            Donation.objects.filter(type_donation='VA', register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(type_donation='RS', register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(type_donation='RE', register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(type_donation='DA', register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(register_at__range=[date_init, date_end]).count()]

        by_typeProcess = [
            Donation.objects.filter(type_process='NO', register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(type_process='NA', register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(type_process='CN', register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(type_process='CA', register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(register_at__range=[date_init, date_end]).count()]

        by_etary = [
            Donation.objects.filter(age_donor__gte=18, age_donor__lte=25,
                                    register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(age_donor__gte=26, age_donor__lte=30,
                                    register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(age_donor__gte=31, age_donor__lte=40,
                                    register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(age_donor__gte=41, age_donor__lte=50,
                                    register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(age_donor__gte=51, age_donor__lte=60,
                                    register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(age_donor__gte=60, age_donor__lte=65,
                                    register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(register_at__range=[date_init, date_end]).count()]

        by_reasonRejected = [
            Donation.objects.filter(rejected__isnull=True, register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(rejected__isnull=False, register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(rejected__reason__type='TE', register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(rejected__reason__type='PE', register_at__range=[date_init, date_end]).count(),
            Donation.objects.filter(register_at__range=[date_init, date_end]).count()]

        # donation_ids = Donation.objects.filter(register_at__range=[date_init, date_end]).values_list('id', flat=True)
        extraction_ids = Extraction.objects.filter(donation__register_at__range=[date_init, date_end]).values_list('id',
                                                                                                                   flat=True)

        typehemocomponents = TypeHemocomponent.objects.filter(show_in_fragmentation=True)
        production = []
        th_ids = []

        for th in typehemocomponents:
            th_ids.append(th.id)
            total = ItemFragmentation.objects.filter(typehemocomponent_id=th.id,
                                                     fragmentation__extraction__in=extraction_ids).count()
            cp = ItemFragmentation.objects.filter(typehemocomponent_id=th.id, typediscard__isnull=False,
                                                  fragmentation__extraction__in=extraction_ids).count()
            sp = ItemFragmentation.objects.filter(typehemocomponent_id=th.id, typediscard__isnull=True,
                                                  fragmentation__extraction__in=extraction_ids).count()

            production.append(
                [
                    th.name,
                    cp,
                    sp,
                    total
                ]
            )
        ItemFragmentation.objects.filter(typehemocomponent__show_in_fragmentation=True)
        totals = ['TOTAL PRODUCIDOS',
                  ItemFragmentation.objects.filter(typehemocomponent__show_in_fragmentation=True,
                                                   typediscard__isnull=False,
                                                   fragmentation__extraction__in=extraction_ids).count(),
                  ItemFragmentation.objects.filter(typehemocomponent__show_in_fragmentation=True,
                                                   typediscard__isnull=True,
                                                   fragmentation__extraction__in=extraction_ids).count(),
                  ItemFragmentation.objects.filter(typehemocomponent__show_in_fragmentation=True,
                                                   fragmentation__extraction__in=extraction_ids).count()
                  ]
        production.append(totals)

        serologies = get_serologies(date_init, date_end)

        params = {
            'today': today,
            'request': request,
            'by_gender': by_gender,
            'by_event': by_event,
            'by_typeDonation': by_typeDonation,
            'by_typeProcess': by_typeProcess,
            'by_etary': by_etary,
            'by_reasonRejected': by_reasonRejected,
            'production': production,
            'serologies': serologies,
            'date_init': date_init,
            'date_end': date_end,

        }
        return Render.render('general-pdf.html', params)


def get_serologies(date_init, date_end):
    serologies = []
    total_serologies = Immunoserology.objects.filter(Q(register_at__range=[date_init, date_end])).count()
    serologies.append(['CHAGAS HAI',
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end], chagas_hai='R').count(),
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end], chagas_hai='NR').count(),
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end],
                                                     chagas_hai__isnull=True).count(),
                       total_serologies
                       ])
    serologies.append(['CHEIA',
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end], cheia='R').count(),
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end], cheia='NR').count(),
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end],
                                                     cheia__isnull=True).count(),
                       total_serologies

                       ])
    serologies.append(['RPR',
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end], rpr='R').count(),
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end], rpr='NR').count(),
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end],
                                                     rpr__isnull=True).count(),
                       total_serologies

                       ])

    serologies.append(['HVC',
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end], hvc='R').count(),
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end], hvc='NR').count(),
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end],
                                                     hvc__isnull=True).count(),
                       total_serologies

                       ])

    serologies.append(['HBsAg',
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end], hbsag='R').count(),
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end], hbsag='NR').count(),
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end],
                                                     hbsag__isnull=True).count(),
                       total_serologies

                       ])
    serologies.append(['HIV',
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end], hiv='R').count(),
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end], hiv='NR').count(),
                       Immunoserology.objects.filter(register_at__range=[date_init, date_end],
                                                     hiv__isnull=True).count(),
                       total_serologies

                       ])
    serologies.append(['TOTALES',
                       Immunoserology.objects.filter(Q(register_at__range=[date_init, date_end]), Q(
                           Q(chagas_hai='R') | Q(cheia='R') | Q(rpr='R') | Q(hvc='R') | Q(hbsag='R') | Q(
                               hiv='R'))).count(),
                       Immunoserology.objects.filter(Q(register_at__range=[date_init, date_end]), Q(
                           Q(chagas_hai='NR') | Q(cheia='NR') | Q(rpr='NR') | Q(hvc='NR') | Q(hbsag='NR') | Q(
                               hiv='NR'))).count(),
                       Immunoserology.objects.filter(Q(register_at__range=[date_init, date_end]), Q(
                           Q(chagas_hai__isnull=True) | Q(cheia__isnull=True) | Q(rpr__isnull=True) | Q(
                               hvc__isnull=True) | Q(hbsag__isnull=True) | Q(
                               hiv__isnull=True))).count(),
                       total_serologies
                       ])

    return serologies


class GeneralDonationPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        donations = Donation.objects.filter(register_at__range=[date_init, date_end]).order_by('register_at',
                                                                                               'donor__code')

        params = {
            'today': today,
            'request': request,
            'donations': donations,
            'date_init': date_init,
            'date_end': date_end
        }

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'general-donation-pdf.html', params)
        else:
            return Render.render_pdf_view('general-donation-pdf.html', params)


class GeneralExamPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']

        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        exams = Exam.objects.filter(created_at__date__range=[date_init, date_end]).order_by('created_at',
                                                                                            'donation__donor__code')
        params = {
            'today': today,
            'request': request,
            'exams': exams,
            'date_init': date_init,
            'date_end': date_end
        }
        return Render.render('general-exam-pdf.html', params)


class GeneralPhysicalAnalysisPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        physicalAnalysis = PhysicalAnalysis.objects.filter(created_at__date__range=[date_init, date_end]).order_by(
            'created_at', 'donation__donor__code')

        params = {
            'today': today,
            'request': request,
            'physicalAnalysis': physicalAnalysis,
            'date_init': date_init,
            'date_end': date_end

        }
        return Render.render('general-physical-analysis-pdf.html', params)


class DailyReleasePDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        releases = Release.objects.filter(register_at__range=[date_init, date_end])
        typehemocomponent_id = request.GET.get('typehemocomponent_id')
        if typehemocomponent_id and typehemocomponent_id.isdigit():
            releases = releases.filter(itemfragmentation__typehemocomponent_id=typehemocomponent_id)
        releases = releases.order_by(
            'itemfragmentation__typehemocomponent__name', 'itemfragmentation__donor_code')

        params = {
            'today': today,
            'request': request,
            'releases': releases,
            'date_init': date_init,
            'date_end': date_end

        }

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'daily/daily-release-pdf.html', params)
        else:
            return Render.render_pdf_view('daily/daily-release-pdf.html', params)


class DailyDiscardActPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        observer = None
        responsible = None
        administrator = None
        director = None
        time = None
        if request.GET['time']:
            time = request.GET['time']
        if request.GET['responsible_id']:
            responsible = Employee.objects.get(id=request.GET['responsible_id'])
        if request.GET['administrator_id']:
            administrator = Employee.objects.get(id=request.GET['administrator_id'])
        if request.GET['observer_id']:
            observer = Employee.objects.get(id=request.GET['observer_id'])
        if request.GET['director_id']:
            director = Employee.objects.get(id=request.GET['director_id'])

        discards = Discard.objects.filter(register_at__range=[date_init, date_end]).order_by(
            'itemfragmentation__typehemocomponent__name')
        params = {
            'today': today,
            'request': request,
            'discards': discards,
            'date_init': date_init,
            'date_end': date_end,
            'observer': observer,
            'administrator': administrator,
            'director': director,
            'responsible': responsible,
            'time': time
        }
        return Render.render('daily/daily-discard-act-pdf.html', params)


class GeneralReleasePDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        releases = Release.objects.filter(register_at__range=[date_init, date_end]).order_by(
            'itemfragmentation__typehemocomponent__name')

        params = {
            'today': today,
            'request': request,
            'releases': releases,
            'date_init': date_init,
            'date_end': date_end

        }
        return Render.render('general-release-pdf.html', params)


class DailyDiscardPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        discards = Discard.objects.filter(register_at__range=[date_init, date_end]).order_by(
            'itemfragmentation__typehemocomponent__name', 'itemfragmentation__donor_code')

        params = {
            'today': today,
            'request': request,
            'discards': discards,
            'date_init': date_init,
            'date_end': date_end

        }

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'daily/daily-discard-pdf.html', params)
        else:
            return Render.render_pdf_view('daily/daily-discard-pdf.html', params)


class GeneralDiscardPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        discards = Discard.objects.filter(register_at__range=[date_init, date_end]).order_by(
            'itemfragmentation__typehemocomponent__name')

        params = {
            'today': today,
            'request': request,
            'discards': discards,
            'date_init': date_init,
            'date_end': date_end

        }
        return Render.render('general-discard-pdf.html', params)


class GeneralReleaseListPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        releases = Release.objects.filter(register_at__range=[date_init, date_end]).order_by(
            'itemfragmentation__typehemocomponent__name')

        params = {
            'today': today,
            'request': request,
            'releases': releases,
            'date_init': date_init,
            'date_end': date_end

        }
        return Render.render('general-release-list-pdf.html', params)


class DonationTimelinePDF(View):

    def get(self, request):
        today = timezone.now()
        donation_id = request.GET['donation_id']
        donation = Donation.objects.get(id=donation_id)

        # donation
        exam = Exam.objects.filter(donation_id=donation_id).first()
        physical_analysis = PhysicalAnalysis.objects.filter(donation_id=donation_id).first()
        clinical_history = ClinicalHistoryAnswer.objects.filter(donation_id=donation_id).first()
        extraction = Extraction.objects.filter(donation_id=donation_id).first()
        immunohematology = Immunohematology.objects.filter(donation_id=donation_id).first()
        immunoserology = Immunoserology.objects.filter(donation_id=donation_id).first()

        # extraction
        self_exclusion = None
        adverse_reaction = None
        extraction_refreshment = None
        fragmentation = None
        itemfragmentations = None
        if extraction:
            self_exclusion = SelfExclusion.objects.filter(extraction_id=extraction.id).first()
            adverse_reaction = AdverseReaction.objects.filter(extraction_id=extraction.id).first()
            extraction_refreshment = ExtractionRefreshment.objects.filter(extraction_id=extraction.id).first()
            fragmentation = Fragmentation.objects.filter(extraction_id=extraction.id).first()

            if fragmentation:
                itemfragmentations = ItemFragmentation.objects.filter(fragmentation_id=fragmentation.id)

        # rejected
        rejected = Rejected.objects.filter(donation_id=donation_id).first()

        params = {
            'today': today,
            'request': request,
            'donation': donation,
            'exam': exam,
            'physical_analysis': physical_analysis,
            'clinical_history': clinical_history,
            'extraction': extraction,
            'self_exclusion': self_exclusion,
            'adverse_reaction': adverse_reaction,
            'extraction_refreshment': extraction_refreshment,
            'immunohematology': immunohematology,
            'immunoserology': immunoserology,
            'fragmentation': fragmentation,
            'itemfragmentations': itemfragmentations,
            'rejected': rejected
        }
        return Render.render('donation-timeline-pdf.html', params)


class GeneralDistributionPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)

        args = {}
        if request.GET['institution_id']:
            args['institution_id'] = request.GET['institution_id']
        if request.GET['type_payment']:
            args['type_payment'] = request.GET['type_payment']
        if request.GET['employee_id']:
            args['employee_id'] = request.GET['employee_id']
        if request.GET['institution__is_public']:
            if request.GET['institution__is_public'] == 'false':
                args['institution__is_public'] = False
            else:
                args['institution__is_public'] = True
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        distributions = Distribution.objects.filter(
            register_at__date__range=[date_init, date_end],
            **args
        )
        distributions = filter_by_age_group(distributions, request.GET.get('age_group'))
        distributions = distributions.order_by('-register_at', 'patient__middle_name', 'patient__first_name')

        params = {
            'today': today,
            'request': request,
            'distributions': distributions,
            'date_init': date_init,
            'date_end': date_end

        }
        return Render.render('distribution/general-distribution-pdf.html', params)


class DailyImmunohematologyPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        immunohematologies = Immunohematology.objects.filter(register_at__range=[date_init, date_end]).order_by(
            'register_at')

        params = {
            'today': today,
            'request': request,
            'immunohematologies': immunohematologies,
            'date_init': date_init,
            'date_end': date_end

        }

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'daily/daily-immunohematology-pdf.html', params)
        else:
            return Render.render_pdf_view('daily/daily-immunohematology-pdf.html', params)


class GeneralImmunohematologyPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        immunohematologies = Immunohematology.objects.filter(register_at__range=[date_init, date_end]).order_by(
            'register_at')
        params = {
            'today': today,
            'request': request,
            'immunohematologies': immunohematologies,
            'date_init': date_init,
            'date_end': date_end

        }
        return Render.render('general/general-immunohematology-pdf.html', params)


class DailyImmunoserologyPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        immunoserologies = Immunoserology.objects.filter(register_at__range=[date_init, date_end]).order_by(
            'register_at')

        params = {
            'today': today,
            'request': request,
            'immunoserologies': immunoserologies,
            'date_init': date_init,
            'date_end': date_end

        }

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'daily/daily-immunoserology-pdf.html', params)
        else:
            return Render.render_pdf_view('daily/daily-immunoserology-pdf.html', params)


class GeneralImmunoserologyPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        immunoserologies = Immunoserology.objects.filter(register_at__range=[date_init, date_end]).order_by(
            'register_at')

        params = {
            'today': today,
            'request': request,
            'immunoserologies': immunoserologies,
            'date_init': date_init,
            'date_end': date_end

        }
        return Render.render('general/general-immunoserology-pdf.html', params)


class GeneralDistributionItemfragmentationPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()
        args = {}
        if request.GET['type_payment']:
            args['distribution__type_payment'] = request.GET['type_payment']

        items = DistributionItemFragmentation.objects.filter(distribution__register_at__range=[date_init, date_end],
                                                             **args).order_by('distribution__register_at')

        params = {
            'today': today,
            'request': request,
            'items': items,
            'date_init': date_init,
            'date_end': date_end

        }
        return Render.render('distribution/general-distribution-itemfragmentation-pdf.html', params)


class DailyDonationPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        args = {}
        if data['event'] and data['event'] == '0':
            args['event__isnull'] = True
        elif data['event'] and data['event'] == '1':
            args['event__isnull'] = False

        donations = Donation.objects.filter(register_at__range=[date_init, date_end], **args).order_by('-donor__code')
        totals = []
        for i in range(1, 22):
            totals.append(0)

        for donation in donations:
            rejected = Rejected.objects.filter(donation_id=donation.id).first()
            extraction = Extraction.objects.filter(donation_id=donation.id).first()
            if donation.donor.gender == 'M':
                totals[0] = totals[0] + 1
            if donation.donor.gender == 'F':
                totals[1] = totals[1] + 1
            if extraction:
                totals[2] = totals[2] + 1
            if extraction is None:
                totals[3] = totals[3] + 1
            if donation.donor.age < 26:
                totals[4] = totals[4] + 1
            if donation.donor.age > 26 and donation.donor.age < 31:
                totals[5] = totals[5] + 1
            if donation.donor.age > 30 and donation.donor.age < 41:
                totals[6] = totals[6] + 1
            if donation.donor.age > 40 and donation.donor.age < 51:
                totals[7] = totals[7] + 1
            if donation.donor.age > 50 and donation.donor.age < 61:
                totals[8] = totals[8] + 1
            if donation.donor.age > 61:
                totals[9] = totals[9] + 1
            if donation.type_donation == 'VA':
                totals[10] = totals[10] + 1
            if donation.type_donation == 'RS':
                totals[11] = totals[11] + 1
            if donation.type_donation == 'RE':
                totals[12] = totals[12] + 1
            if donation.type_donation == 'DA':
                totals[13] = totals[13] + 1
            if donation.exam.hematocrit:
                totals[14] = totals[14] + 1
            if donation.exam.blood_group:
                totals[15] = totals[15] + 1
            if donation.exam.rpr:
                totals[16] = totals[16] + 1
            if donation.exam.chagas:
                totals[17] = totals[17] + 1
            if rejected and rejected.resource == 'Exam':
                totals[18] = totals[18] + 1
            if rejected and rejected.resource == 'PhysicalAnaysis':
                totals[19] = totals[19] + 1
            if rejected and rejected.resource == 'ClinicalHistory':
                totals[20] = totals[20] + 1

        params = {
            'today': today,
            'request': request,
            'donations': donations,
            'date_init': date_init,
            'date_end': date_end,
            'totals': totals
        }

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'daily/daily-donation-pdf.html', params)
        else:
            return Render.render_pdf_view('daily/daily-donation-pdf.html', params)


class DailyFragmentationPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        args = {}
        if data['employee_id']:
            args['employee_id'] = data['employee_id']

        fragmentations = Fragmentation.objects.filter(register_at__range=[date_init, date_end], **args).order_by('-id')
        totals = [0] * 21
        bag_type_indexes = {
            'SIMPLE': 0,
            'DOBLE': 1,
            'TRIPLE': 2,
            'CUADRUPLE': 3,
            'CUADRUPLE_CON_FILTRO': 4,
            'SET_AFERESIS': 5,
        }

        for fragmentation in fragmentations:
            bag_type_index = bag_type_indexes.get(fragmentation.extraction.type_bag)
            if bag_type_index is not None:
                totals[bag_type_index] += 1
            if get_hemocomponent_from_fragmentation(fragmentation.id, hemocomponent_id=1) == 'X':
                totals[6] += 1
            if get_hemocomponent_from_fragmentation(fragmentation.id, hemocomponent_id=2) == 'X':
                totals[7] += 1
            if get_hemocomponent_from_fragmentation(fragmentation.id, hemocomponent_id=3) == 'X':
                totals[8] += 1
            if get_hemocomponent_from_fragmentation(fragmentation.id, hemocomponent_id=4) == 'X':
                totals[9] += 1
            if get_hemocomponent_from_fragmentation(fragmentation.id, hemocomponent_id=5) == 'X':
                totals[10] += 1
            if get_hemocomponent_from_fragmentation(fragmentation.id, hemocomponent_id=6) == 'X':
                totals[11] += 1
            if get_hemocomponent_from_fragmentation(fragmentation.id, hemocomponent_id=7) == 'X':
                totals[12] += 1
            if get_hemocomponent_from_fragmentation(fragmentation.id, hemocomponent_id=8) == 'X':
                totals[13] += 1
            if get_hemocomponent_from_fragmentation(fragmentation.id, hemocomponent_id=9) == 'X':
                totals[14] += 1
            if get_hemocomponent_from_fragmentation(fragmentation.id, hemocomponent_id=10) == 'X':
                totals[15] += 1
            if get_hemocomponent_from_fragmentation(fragmentation.id, hemocomponent_id=11) == 'X':
                totals[16] += 1
            if get_hemocomponent_from_fragmentation(fragmentation.id, hemocomponent_id=12) == 'X':
                totals[17] += 1
            if get_hemocomponent_from_fragmentation(fragmentation.id, hemocomponent_id=13) == 'X':
                totals[18] += 1
            if get_hemocomponent_from_fragmentation(fragmentation.id, hemocomponent_id=15) == 'X':
                totals[19] += 1
            if get_hemocomponent_from_fragmentation(fragmentation.id, hemocomponent_id=16) == 'X':
                totals[20] += 1
        params = {
            'today': today,
            'request': request,
            'fragmentations': fragmentations,
            'date_init': date_init,
            'date_end': date_end,
            'totals': totals
        }

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'daily/daily-fragmentation-pdf.html', params)
        else:
            return Render.render_pdf_view('daily/daily-fragmentation-pdf.html', params)


class DailyProductionPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        productions = ItemFragmentation.objects.exclude(release__isnull=True, discard__isnull=True).filter(
            register_at__range=[date_init, date_end]).order_by('-id')

        totals = []
        for i in range(1, 18):
            totals.append(0)

        for production in productions:
            if production.typehemocomponent.id == 1:
                totals[0] = totals[0] + 1
            if production.typehemocomponent.id == 2:
                totals[1] = totals[1] + 1
            if production.typehemocomponent.id == 3:
                totals[2] = totals[2] + 1
            if production.typehemocomponent.id == 4:
                totals[3] = totals[3] + 1
            if production.typehemocomponent.id == 5:
                totals[4] = totals[4] + 1
            if production.typehemocomponent.id == 6:
                totals[5] = totals[5] + 1
            if production.typehemocomponent.id == 7:
                totals[6] = totals[6] + 1
            if production.typehemocomponent.id == 8:
                totals[7] = totals[7] + 1
            if production.typehemocomponent.id == 9:
                totals[8] = totals[8] + 1
            if production.typehemocomponent.id == 10:
                totals[9] = totals[9] + 1
            if production.typehemocomponent.id == 11:
                totals[10] = totals[10] + 1
            if production.typehemocomponent.id == 12:
                totals[11] = totals[11] + 1
            if production.typehemocomponent.id == 13:
                totals[12] = totals[12] + 1
            if production.typehemocomponent.id == 15:
                totals[13] = totals[13] + 1
            if production.typehemocomponent.id == 16:
                totals[14] = totals[14] + 1
            if get_release_for_item(production):
                totals[15] = totals[15] + 1
            if get_discard_for_item(production):
                totals[16] = totals[16] + 1

        params = {
            'today': today,
            'request': request,
            'productions': productions,
            'date_init': date_init,
            'date_end': date_end,
            'totals': totals
        }

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'daily/daily-production-pdf.html', params)
        else:
            return Render.render_pdf_view('daily/daily-production-pdf.html', params)


class DailyDistributionPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['extra']
        data = json.loads(extra)
        date_init = datetime.strptime(data['date_init'], "%Y-%m-%d").date()
        date_end = datetime.strptime(data['date_end'], "%Y-%m-%d").date()

        distributions = Distribution.objects.filter(register_at__date__range=[date_init, date_end]).order_by('-id')

        totals = []
        for i in range(1, 6):
            totals.append(0)

        for distribution in distributions:
            if distribution.institution is None:
                totals[0] = totals[0] + 1
            if distribution.institution:
                totals[1] = totals[1] + 1
            if distribution.type_payment == 0:
                totals[2] = totals[2] + 1
            if distribution.type_payment == 1:
                totals[3] = totals[3] + 1
            if len(get_itemfragmentations(distribution.id)):
                totals[4] = totals[4] + len(get_itemfragmentations(distribution.id))

        params = {
            'today': today,
            'request': request,
            'distributions': distributions,
            'date_init': date_init,
            'date_end': date_end,
            'totals': totals
        }

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'daily/daily-distribution-pdf.html', params)
        else:
            return Render.render_pdf_view('daily/daily-distribution-pdf.html', params)
