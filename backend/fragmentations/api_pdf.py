from siicobs_main.render import Render
from django.shortcuts import render

from fragmentations.models import ItemFragmentation
from django.utils import timezone
from django.views.generic import View


class RoadMap(View):

    def get(self, request):
        params = {}

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'road-map-pdf.html', params)
        else:
            return Render.render('road-map-pdf.html', params)


class MassiveBloodBagPDF(View):

    def get(self, request):
        today = timezone.now()
        extra = request.GET['0']
        data = extra.split(',')

        items = ItemFragmentation.objects.filter(pk__in=data).order_by(
            'typehemocomponent__name')

        params = {
            'today': today,
            'request': request,
            'items': items,

        }

        format = request.GET.get('format', 'pdf')

        if format == 'html':
            return render(request, 'massive-blood-bags.html', params)
        else:
            return Render.render('massive-blood-bags.html', params)

