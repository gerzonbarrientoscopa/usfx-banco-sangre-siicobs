from django.urls import path

from fragmentations.api_pdf import RoadMap, MassiveBloodBagPDF


urlpatterns = [
    path('api/v1/fragmentations/road-map/pdf/', RoadMap.as_view()),
    path('api/v1/release-massive-bags-pdf/', MassiveBloodBagPDF.as_view()),
]
