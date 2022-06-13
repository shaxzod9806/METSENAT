from django.contrib import admin
from .models import Student, Sponsor, OTM

# Register your models here.
admin.site.register(OTM)
admin.site.register(Sponsor)
admin.site.register(Student)
