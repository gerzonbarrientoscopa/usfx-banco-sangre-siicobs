from django.contrib import admin

from distributions.models import Distribution, DistributionItemFragmentation

admin.site.register(Distribution)
admin.site.register(DistributionItemFragmentation)