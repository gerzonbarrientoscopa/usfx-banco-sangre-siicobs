from django.urls import path

from distributions.api_pdf import DistributionReport, RequestReportGlobal, RequestReportParticular


urlpatterns = [
    path('api/v1/distributions/<int:id>/pdf/', DistributionReport.as_view()),
    path('api/v1/distributions-request-global-pdf/', RequestReportGlobal.as_view()),
    path('api/v1/distributions-request-particular-pdf/', RequestReportParticular.as_view()),
]
