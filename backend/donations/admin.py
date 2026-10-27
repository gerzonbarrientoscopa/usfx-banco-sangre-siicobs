from django.contrib import admin

from donations.models import Donation, Rejected, PhysicalAnalysis, Exam

admin.site.register(Donation)
admin.site.register(Rejected)
admin.site.register(PhysicalAnalysis)
admin.site.register(Exam)
