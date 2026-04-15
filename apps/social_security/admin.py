from django.contrib import admin
from .models import SocialSecurityRecord


@admin.register(SocialSecurityRecord)
class SocialSecurityAdmin(admin.ModelAdmin):
    list_display  = ['masked_ssn', 'person', 'status', 'issue_date']
    list_filter   = ['status']
    search_fields = ['person__first_name', 'person__last_name']