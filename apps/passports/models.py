from django.db import models
from django.conf import settings
from apps.persons.models import Person


class Passport(models.Model):

    PASSPORT_TYPE_CHOICES = [
        ("REGULAR",    "Regular"),
        ("OFFICIAL",   "Official"),
        ("DIPLOMATIC", "Diplomatic"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE",    "Active"),
        ("EXPIRED",   "Expired"),
        ("REVOKED",   "Revoked"),
        ("SUSPENDED", "Suspended"),
        ("LOST",      "Lost/Stolen"),
    ]

    person            = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="passport")
    passport_number   = models.CharField(max_length=20, unique=True)
    passport_type     = models.CharField(max_length=20, choices=PASSPORT_TYPE_CHOICES, default="REGULAR")
    issuing_authority = models.CharField(max_length=255, default="U.S. Department of State")
    issue_date        = models.DateField()
    expiration_date   = models.DateField()
    status            = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    issued_by         = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="passports_issued"
    )
    notes      = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.passport_number} - {self.person} ({self.status})"