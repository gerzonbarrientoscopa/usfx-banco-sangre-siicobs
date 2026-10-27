from django.urls import path

from donors.api_pdf import PreSieveAll, Autoexclude, AdverseReactionHistory, ClinicalHistoryQuestion
from .api_pdf import ClinicalHistory

urlpatterns = [
    path('api/v1/donations/<int:id>/pdf/', ClinicalHistory.as_view()),
    path('api/v1/clinical-histories/<int:id>/pdf/answers', ClinicalHistoryQuestion.as_view()),
    path('api/v1/adverse-reactions/<int:id>/pdf/', AdverseReactionHistory.as_view()),
    path('api/v1/extractions/<int:id>/pdf/', Autoexclude.as_view()),
    path('api/v1/exams/presieve/pdf/', PreSieveAll.as_view()),
]
