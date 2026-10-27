from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from donations.models import Donation
from django.db.models.functions import TruncMonth
from django.db.models import Count


class ByYearView(APIView):
    def get(self, request, *args, **kwargs):
        year = request.query_params.get('year', None)
        start_date = year + '-01-01'
        end_date = year + '-12-31'
        if (year):
            totals = Donation.objects.filter(register_at__range=[start_date, end_date]).annotate(
                month=TruncMonth('register_at')).values('month').annotate(
                total=Count('id')).order_by('month')
            total_f = Donation.objects.filter(register_at__range=[start_date, end_date],
                                              donor__gender='M').annotate(month=TruncMonth('register_at')).values(
                'month').annotate(
                total=Count('id')).order_by('month')
            total_m = Donation.objects.filter(register_at__range=[start_date, end_date],
                                              donor__gender='F').annotate(month=TruncMonth('register_at')).values(
                'month').annotate(
                total=Count('id')).order_by('month')
            for total in totals:
                for t_m in total_m:
                    if total['month'] == t_m['month']:
                        total['m'] = t_m['total']
                for t_m in total_f:
                    if total['month'] == t_m['month']:
                        total['f'] = t_m['total']

            return Response({'data': totals}, status=status.HTTP_200_OK)
