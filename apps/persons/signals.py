"""
apps/persons/signals.py

Auto-creates an IDApplication when a new Person record is saved
if the person is 16 years of age or older.

Why signals instead of the view?
  Signals fire regardless of HOW the person was created — via the
  API, the Django admin, a Celery task, or the birth-records
  inline-create flow. Views can be bypassed; signals cannot.

Flow:
  post_save → Person created → age >= 16 → IDApplication(FIRST_TIME_ID, DRAFT)

The application is created with status DRAFT so that a DMV officer
must review and approve it before an ID is physically issued.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date


@receiver(post_save, sender='persons.Person')
def auto_create_id_application(sender, instance, created, **kwargs):
    """
    Fires after every Person save.
    Only acts on newly-created records (created=True).
    Only creates an application if the person is 16 or older.
    Does nothing if an application already exists for this person
    (guards against duplicate signals or manual re-saves).
    """
    if not created:
        return  # Only run on initial creation, not every save

    # ── Age gate ─────────────────────────────────────────────────
    today = date.today()
    dob   = instance.date_of_birth

    # Calculate age in full years
    age = (today - dob).days // 365

    if age < 16:
        return  # Person is too young for an ID application

    # ── Guard: don't create a duplicate ──────────────────────────
    # Import here (inside the function) to avoid circular imports
    # at module load time — the apps may not be fully registered yet.
    from apps.id_applications.models import IDApplication

    if IDApplication.objects.filter(person=instance).exists():
        return  # Already has an application on record

    # ── Create the application ───────────────────────────────────
    IDApplication.objects.create(
        person           = instance,
        application_type = 'FIRST_TIME_ID',   # Always first-time for new persons
        status           = 'DRAFT',            # DMV must review before approving
        state_of_issue   = instance.address_state or '',  # Pre-fill from address if available
    )