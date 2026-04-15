from django.contrib import admin
from .models import PersonPhoto


@admin.register(PersonPhoto)
class PersonPhotoAdmin(admin.ModelAdmin):
    list_display  = ['person', 'purpose', 'is_current', 'uploaded_by', 'uploaded_at']
    list_filter   = ['purpose', 'is_current']
    search_fields = ['person__first_name', 'person__last_name']