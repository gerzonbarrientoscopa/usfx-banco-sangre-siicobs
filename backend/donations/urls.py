from django.urls import path

from donations.api_pdf import DonationBCPdf

urlpatterns = [
    path('api/v1/donation-bc/<int:id>/<int:quantity>/pdf/', DonationBCPdf.as_view()),
]
