from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View

from donations.models import Donation
from fragmentations.models import ItemFragmentation, Fragmentation, Release
from laboratories.models import SerologyProtocol, Immunoserology, Immunohematology
from siicobs_main.render import Render
from siicobs_main.utils_billing import build_picture_qr, build_picture_barcode, build_picture_barcode_bg, \
    build_picture_barcode_prod_bg


class BloodBag(View):

    def get(self, request, id):
        itemfragmentation = ItemFragmentation.objects.get(id=id)
        fragmentation = Fragmentation.objects.get(id=itemfragmentation.fragmentation_id)
        donation = Donation.objects.get(id=fragmentation.extraction.donation_id)
        immunohematology = Immunohematology.objects.get(donation_id=donation.id)
        immunoserology = Immunoserology.objects.get(donation_id=donation.id)
        release = Release.objects.get(itemfragmentation_id=itemfragmentation.id)

        message_antikell = ''
        if immunohematology and immunohematology.antikell != '-':
            message_antikell = 'Transfundir a personas de la tercera edad.'

        blood_group = immunohematology.direct_abo
        factor_rh = immunohematology.factor_rh

        if blood_group == 'A1':
            blood_group = 'A<sub>1</sub>'
        elif blood_group == 'A2':
            blood_group = 'A<sub>2</sub>'
        elif blood_group == 'A1B':
            blood_group = 'A<sub>1</sub>B'
        elif blood_group == 'A2B':
            blood_group = 'A<sub>2</sub>B'

        if factor_rh == 'RH-':
            factor_rh_text = 'Rh D NEGATIVO'
        elif factor_rh == 'RH+':
            factor_rh_text = 'Rh D POSITIVO'
        else:
            factor_rh_text = 'Rh D POSITIVO <br> Du Débil'

        today = timezone.now()
        donor_code = donation.donor.code
        production_bc_id = id
        production_bc_file_name = str(id) + '_1'

        save = build_picture_barcode_bg(str(donation.id).strip(), str(donor_code))
        save = build_picture_barcode_prod_bg(str(production_bc_id).strip(), production_bc_file_name)

        params = {
            'id': str(id),
            'today': today,
            'blood_group': blood_group,
            'factor_rh_text': factor_rh_text,
            'message_antikell': message_antikell,
            'itemfragmentation': itemfragmentation,
            'fragmentation': fragmentation,
            'donation': donation,
            'immunohematology': immunohematology,
            'immunoserology': immunoserology,
            'release': release,
            'donor_code': donor_code,
            'production_bc_file_name': production_bc_file_name,
        }
        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'blood-bag-pdf.html', params)
        else:
            return Render.render('blood-bag-pdf.html', params)


class SerologyProtocolPdf(View):

    def get(self, request, id):
        protocol = SerologyProtocol.objects.get(pk=id)
        today = timezone.now()
        save = build_picture_qr(str(protocol.id), str(protocol.id), 'protocol-serology')
        params = {
            'today': today,
            'protocol': protocol,
            'protocol_obj': SerologyProtocol,
            'range_row': range(12),
            'request': request
        }

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'serology-protocol-pdf.html', params)
        else:
            return Render.render('serology-protocol-pdf.html', params)
