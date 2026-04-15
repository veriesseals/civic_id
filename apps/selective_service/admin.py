from django.contrib import admin
from .models import SelectiveServiceRegistration


@admin.register(SelectiveServiceRegistration)
class SelectiveServiceAdmin(admin.ModelAdmin):
    list_display  = ['registration_number', 'person', 'status', 'registration_date', 'registration_method']
    list_filter   = ['status', 'registration_method', 'is_exempt']
    search_fields = ['registration_number', 'person__first_name', 'person__last_name']