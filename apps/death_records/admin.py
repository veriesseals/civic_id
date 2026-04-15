from django.contrib import admin
from .models import DeathRecord


@admin.register(DeathRecord)
class DeathRecordAdmin(admin.ModelAdmin):
    list_display = ['certificate_number', 'person', 'date_of_death', 'cause_category', 'filed_by']
    list_filter  = ['cause_category']
    search_fields = ['certificate_number', 'person__first_name', 'person__last_name']