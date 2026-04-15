from django.contrib import admin
from .models import MarriageCertificate


@admin.register(MarriageCertificate)
class MarriageCertificateAdmin(admin.ModelAdmin):
    list_display  = ['certificate_number', 'spouse_1', 'spouse_2', 'date_of_marriage', 'status']
    list_filter   = ['status']
    search_fields = ['certificate_number', 'spouse_1__last_name', 'spouse_2__last_name']