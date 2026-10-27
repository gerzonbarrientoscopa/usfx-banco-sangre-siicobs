from django.contrib import admin
from sieves.models import ClinicalHistoryQuestion, ClinicalHistoryAnswer

admin.site.register(ClinicalHistoryQuestion)
admin.site.register(ClinicalHistoryAnswer)
