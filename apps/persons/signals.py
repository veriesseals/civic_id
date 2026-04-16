"""
apps/persons/signals.py

Auto-creates an IDApplication when a new Person record is saved
if the person is 16 years of age or older.

Why signals instead of the view?
  Signals fire regardless of HOW the person was created — via the API,
  the Django admin, a Celery task, or the birth-records inline-create flow.
  Views can be bypassed; signals cannot.

Flow:
  post_save → Person created → age >= 16 → IDApplication(FIRST_TIME_ID, DRAFT)
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from apps.persons.models import Person  # direct import — more reliable than string form


@receiver(post_save, sender=Person)
def auto_create_id_application(sender, instance, created, **kwargs):
    """
    Fires after every Person save.
    Only acts on newly-created records (created=True).
    Only creates an application if the person is 16 or older.
    Does nothing if an application already exists (guards against
    duplicate signals or manual re-saves).
    """
    if not created:
        return  # Only run on initial creation, not every save

    # Age gate
    today = date.today()
    age   = (today - instance.date_of_birth).days // 365
    if age < 16:
        return

    # Import inside function to avoid circular imports at module load time
    from apps.id_applications.models import IDApplication

    if IDApplication.objects.filter(person=instance).exists():
        return  # Guard against duplicates

    IDApplication.objects.create(
        person           = instance,
        application_type = 'FIRST_TIME_ID',
        status           = 'DRAFT',
        state_of_issue   = instance.address_state or '',
    )