from django.contrib import admin
from .models import Student, Sponsor, OTM

# Register your models here.
admin.site.register(OTM)
# admin.site.register(Sponsor)
admin.site.register(Student)


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'phone_number',
                    'sponsorship_amount',
                    'payment_type',
                    'sponsor_type',
                    'company_name',
                    'sponsor_image',
                    'application_status',
                    'created_at',
                    'updated_at',)
    list_filter = ('name',
                   'phone_number',
                   'sponsorship_amount',
                   'payment_type',
                   'sponsor_type',
                   'company_name',
                   'sponsor_image',
                   'application_status',
                   'created_at',
                   'updated_at',)
    search_fields = ('name',
                     'phone_number',
                     'sponsorship_amount',
                     'payment_type',
                     'sponsor_type',
                     'company_name',
                     'sponsor_image',
                     'application_status',
                     'created_at',
                     'updated_at',)
    ordering = ('name',
                'phone_number',
                'sponsorship_amount',
                'payment_type',
                'sponsor_type',
                'company_name',
                'sponsor_image',
                'application_status',
                'created_at',
                'updated_at',
                )
