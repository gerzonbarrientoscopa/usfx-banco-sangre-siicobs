from django.contrib import admin

from packages.models import Package, TypeHemocomponent, TypeDiscard

admin.site.register(Package)
admin.site.register(TypeHemocomponent)
admin.site.register(TypeDiscard)

