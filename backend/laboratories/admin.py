from django.contrib import admin
from laboratories.models import Immunohematology, Immunoserology, SerologyProtocol

admin.site.register(Immunohematology)
admin.site.register(Immunoserology)
admin.site.register(SerologyProtocol)
