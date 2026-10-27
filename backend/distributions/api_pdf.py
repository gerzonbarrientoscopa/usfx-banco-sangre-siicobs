from django.utils import timezone
from django.views.generic import View
from django.shortcuts import render

from distributions.models import Distribution, DistributionItemFragmentation
from siicobs_main.render import Render
from siicobs_main.utils_billing import build_picture_qr


class DistributionReport(View):

    def get(self, request, id):
        distribution = Distribution.objects.get(pk=id)
        distributionItemFragmentations = DistributionItemFragmentation.objects.filter(distribution=id)
        distributionItemFragmentationsQuantity = DistributionItemFragmentation.objects.filter(distribution=id).count()
        today = timezone.now()
        save = build_picture_qr(str(distribution.uuid), str(distribution.uuid), 'distribution')

        if distributionItemFragmentationsQuantity < 1:
            extraRows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        else:
            extraRows = [0, 1, 2, 3, 4, 5]
        params = {
            'today': today,
            'distribution': distribution,
            'distribution_obj': Distribution,
            'distributionItemFragmentations': distributionItemFragmentations,
            'request': request,
            'distributionItemFragmentations_obj': DistributionItemFragmentation,
            'extraRows': extraRows
        }

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'distributions/distribution-pdf.html', params)
        else:
            return Render.render('distributions/distribution-pdf.html', params)


class RequestReportGlobal(View):

    def get(self, request):
        today = timezone.now()
        params = {
            'today': today,
            'request': request,
            'quantity': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        }

        format = request.GET.get('format', 'pdf')
        return Render.render('distributions/request-global-pdf.html', params)


class RequestReportParticular(View):

    def get(self, request):
        today = timezone.now()
        params = {
            'today': today,
            'request': request,
            'quantity': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        }

        format = request.GET.get('format', 'pdf')
        return Render.render('distributions/request-particular-pdf.html', params)
