from django.db import models
from persons.models import Person

# Create your models here.
# ------------------------------------------

class ImmigrationStatus(models.Model):
    STATUS_TYPE_CHOICES = [
        ("PERMANENT_RESIDENT", "Permanent Resident"),
        ("VISA_HOLDER", "Visa Holder"),
        ("OTHER_LAWFUL_STATUS", "Other Lawful Status" ),
        
        
        
    ]
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="immigration_statuses")

    status_type = models.CharField(max_length=50, choices=STATUS_TYPE_CHOICES)
    status_start_date = models.DateField()
    status_end_date = models.DateField(blank=True, null=True)
    issuing_authority = models.CharField(max_length=255)
    reference_number = models.CharField(max_length=20, default="PENDING")


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person} - {self.status_type}"