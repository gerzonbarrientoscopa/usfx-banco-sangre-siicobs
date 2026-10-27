from django.contrib import admin

from users.models import Employee, Institution

admin.site.register(Institution)
admin.site.register(Employee)