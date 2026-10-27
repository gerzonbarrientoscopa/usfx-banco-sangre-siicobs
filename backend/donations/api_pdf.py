from django.shortcuts import render
from django.views.generic import View
from donations.models import Donation
from siicobs_main.render import Render
from siicobs_main.utils_billing import build_picture_barcode


class DonationBCPdf(View):

    def get(self, request, id, quantity):
        donation = Donation.objects.get(id=id)
        donor_code = str(donation.donor.code)
        id_str = str(id).strip()
        text_0_missing = 12 - len(id_str)
        barcode = '01' + (text_0_missing * '0') + id_str
        barcode_label = donor_code + ' ' + barcode

        save = build_picture_barcode(barcode, str(barcode), barcode_label)
        params = {
            'register_at': donation.register_at,
            'request': request,
            'donor_code': donor_code,
            'range': range(quantity),
            'barcode': barcode
        }

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'donations/extraction-bc-pdf.html', params)
        else:
            return Render.render('donations/extraction-bc-pdf.html', params)
