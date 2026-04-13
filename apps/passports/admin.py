from django.contrib import admin
from .models import Passport


@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):
    list_display  = ["passport_number", "person", "passport_type", "status", "issue_date", "expiration_date"]
    list_filter   = ["status", "passport_type"]
    search_fields = ["passport_number", "person__first_name", "person__last_name"]
