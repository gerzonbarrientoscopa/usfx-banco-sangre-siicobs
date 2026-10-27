from django.contrib import admin
from fragmentations.models import Fragmentation, ItemFragmentation, Discard, Release, ReleaseRequest, \
    TypeIrregularAntiBody

admin.site.register(Fragmentation)
admin.site.register(ItemFragmentation)
admin.site.register(Discard)
admin.site.register(Release)
admin.site.register(ReleaseRequest)
admin.site.register(TypeIrregularAntiBody)
