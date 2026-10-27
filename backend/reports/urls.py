from django.urls import include, re_path, path

from django.views.decorators.csrf import csrf_exempt

from reports.api_pdf import GeneralPDF, GeneralDonationPDF, GeneralExamPDF, GeneralPhysicalAnalysisPDF, \
    GeneralReleasePDF, DailyReleasePDF, GeneralReleaseListPDF, DonationTimelinePDF, GeneralDistributionPDF, \
    GeneralDiscardPDF, DailyDiscardPDF, DailyDiscardActPDF, DailyImmunohematologyPDF, GeneralImmunohematologyPDF, \
    DailyImmunoserologyPDF, GeneralImmunoserologyPDF, GeneralDistributionItemfragmentationPDF, DailyDonationPDF, \
    DailyFragmentationPDF, DailyProductionPDF, DailyDistributionPDF

from reports.api import ByYearView

urlpatterns = [
    path('api/v1/reports/by-year/', csrf_exempt(ByYearView.as_view())),
    path('api/v1/reports-pdf/', csrf_exempt(GeneralPDF.as_view())),
    path('api/v1/reports-donation-pdf/', csrf_exempt(GeneralDonationPDF.as_view())),
    path('api/v1/reports-exam-pdf/', csrf_exempt(GeneralExamPDF.as_view())),
    path('api/v1/reports-physical-analysis-pdf/', csrf_exempt(GeneralPhysicalAnalysisPDF.as_view())),
    path('api/v1/release-today-pdf/', csrf_exempt(DailyReleasePDF.as_view())),
    path('api/v1/reports-releases-pdf/', csrf_exempt(GeneralReleasePDF.as_view())),
    path('api/v1/discard-today-pdf/', csrf_exempt(DailyDiscardPDF.as_view())),
    path('api/v1/act_discard-today-pdf/', csrf_exempt(DailyDiscardActPDF.as_view())),
    path('api/v1/reports-discards-pdf/', csrf_exempt(GeneralDiscardPDF.as_view())),
    path('api/v1/reports-releases-list-pdf/', csrf_exempt(GeneralReleaseListPDF.as_view())),
    path('api/v1/donation-timeline-pdf/', csrf_exempt(DonationTimelinePDF.as_view())),
    path('api/v1/reports-distributions-pdf/', csrf_exempt(GeneralDistributionPDF.as_view())),
    path('api/v1/reports-distribution-itemfragmentations-pdf/', csrf_exempt(GeneralDistributionItemfragmentationPDF.as_view())),

    path('api/v1/immunohematology-today-pdf/', csrf_exempt(DailyImmunohematologyPDF.as_view())),
    path('api/v1/reports-immunohematologies-pdf/', csrf_exempt(GeneralImmunohematologyPDF.as_view())),
    path('api/v1/immunoserology-today-pdf/', csrf_exempt(DailyImmunoserologyPDF.as_view())),
    path('api/v1/reports-immunoserologies-pdf/', csrf_exempt(GeneralImmunoserologyPDF.as_view())),

    path('api/v1/donation-today-pdf/', csrf_exempt(DailyDonationPDF.as_view())),
    path('api/v1/fragmentation-today-pdf/', csrf_exempt(DailyFragmentationPDF.as_view())),
    path('api/v1/production-today-pdf/', csrf_exempt(DailyProductionPDF.as_view())),
    path('api/v1/distribution-today-pdf/', csrf_exempt(DailyDistributionPDF.as_view())),

]
