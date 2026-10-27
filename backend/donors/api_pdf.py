from django.shortcuts import render
from sieves.models import ClinicalHistoryAnswer

from django.utils import timezone
from django.views.generic import View
from donations.models import Donation, PhysicalAnalysis, Exam, Rejected
from extractions.models import AdverseReaction, Extraction
from donors.models import Donor
from siicobs_main.render import Render
from siicobs_main.utils_billing import build_picture_qr


class ClinicalHistory(View):

    def get(self, request, id):
        today = timezone.now()

        donation = Donation.objects.get(pk=id)
        physical_analysis = PhysicalAnalysis.objects.get(donation=donation)
        exam = Exam.objects.get(donation=donation)
        rejected = Rejected.objects.filter(donation=donation).first()

        save = build_picture_qr(str(donation.donor.code), str(donation.donor.code), 'clinical-history')
        params = {
            'today': today,
            'donation': donation,
            'exam': exam,
            'physical_analysis': physical_analysis,
            'rejected': rejected,
            'request': request,
            'donor_obj': Donor,
            'exam_obj': Exam,
            'pa_obj': PhysicalAnalysis
        }

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'donations/clinical-history-pdf.html', params)
        else:
            return Render.render('donations/clinical-history-pdf.html', params)


class ClinicalHistoryQuestion(View):

    def get(self, request, id):
        cha = ClinicalHistoryAnswer.objects.get(pk=id)
        donation = Donation.objects.get(pk=cha.donation.id)
        donor = Donor.objects.get(pk=donation.donor_id)
        today = timezone.now()
        physical_analysis = PhysicalAnalysis.objects.filter(donation=donation).first()
        rejected = Rejected.objects.filter(donation=donation).first()
        model_pa = PhysicalAnalysis
        save = build_picture_qr(str(donor.code), str(donor.code), 'clinical-history')
        params = {
            'today': today,
            'donations': donation,
            'donor': donor,
            'request': request,
            'instance_model': Donor,
            'physical_analysis': physical_analysis,
            'model_pa': model_pa,
            'rejected': rejected,
            'cha': cha
        }

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'donations/clinical-history-2-pdf.html', params)
        else:
            return Render.render('donations/clinical-history-2-pdf.html', params)


class PreSieveAll(View):

    def get(self, request):
        today = timezone.now()
        params = {
            'today': today,
        }

        return Render.render('donations/pre-sieve-laboratorial-pdf.html', params)


class AdverseReactionHistory(View):

    def get(self, request, id):
        adverse_reactions = AdverseReaction.objects.get(pk=id)
        extraction = Extraction.objects.get(pk=adverse_reactions.extraction_id)
        donation = Donation.objects.get(pk=extraction.donation_id)
        today = timezone.now()
        save = build_picture_qr(str(donation.donor.code), str(donation.donor.code), 'donor')
        params = {
            'today': today,
            'donation': donation,
            'donations_obj': Donation,
            'request': request,
            'donor_obj': Donor,
            'adverse_reactions': adverse_reactions,
            'ar_obj': AdverseReaction
        }

        return Render.render('donations/adverse-reaction-pdf.html', params)


class Autoexclude(View):

    def get(self, request, id):
        donation = Donation.objects.get(pk=id)
        today = timezone.now()
        extraction = Extraction.objects.filter(donation=donation)
        save = build_picture_qr(str(donation.donor.code), str(donation.donor.code), 'donor')
        params = {
            'today': today,
            'donation': donation,
            'donations_obj': Donation,
            'request': request,
            'instance_model': Donor,
            'extraction': extraction,
            'model_ar': Extraction
        }

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'donations/auto-exclude-pdf.html', params)
        else:
            return Render.render('donations/auto-exclude-pdf.html', params)
