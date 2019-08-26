from django.contrib import admin
from main.models import question,answer,reportques,reportans
from main.models import msgs
# Register your models here.
# Register your models here.
admin.site.register(question)
admin.site.register(answer)
admin.site.register(reportques)
admin.site.register(reportans)
admin.site.register(msgs)