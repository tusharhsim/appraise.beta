from django.contrib import admin

from .models import Person, RequestService, ProvideService, JobAlert, HiringAlert

admin.site.register(Person)
admin.site.register(RequestService)
admin.site.register(ProvideService)
admin.site.register(JobAlert)
admin.site.register(HiringAlert)