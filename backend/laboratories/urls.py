from django.urls import path

from laboratories.api_pdf import BloodBag, SerologyProtocolPdf


urlpatterns = [
    path('api/v1/laboratories/bloodbag/<int:id>/pdf/', BloodBag.as_view()),
    path('api/v1/serology-protocols/<int:id>/pdf/', SerologyProtocolPdf.as_view()),
]
