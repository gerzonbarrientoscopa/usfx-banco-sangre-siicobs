from django.contrib import admin

from extractions.models import Extraction, SelfExclusion, TypeAdverseReaction, AdverseReaction

admin.site.register(Extraction)
admin.site.register(SelfExclusion)
admin.site.register(TypeAdverseReaction)
admin.site.register(AdverseReaction)
