from celery import shared_task
from datetime import date
import logging

logger = logging.getLogger(__name__)


@shared_task(name='apps.civic_tasks.tasks.run_daily_civic_checks')
def run_daily_civic_checks():
    """
    Master daily task. Runs all age-triggered civic registrations.
    Fired every day at midnight UTC by Celery Beat.
    """
    today = date.today()
    logger.info(f"[CivicTasks] Running daily checks for {today}")

    results = {
        'date': str(today),
        'voter_registrations': 0,
        'selective_service_registrations': 0,
        'errors': [],
    }

    from apps.persons.models import Person
    turning_18 = Person.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day,
        date_of_birth__year=today.year - 18,
        date_of_death__isnull=True,
    )

    logger.info(f"[CivicTasks] Found {turning_18.count()} persons turning 18 today")

    for person in turning_18:
        try:
            if auto_register_voter(person):
                results['voter_registrations'] += 1
        except Exception as e:
            msg = f"Voter reg failed for Person #{person.id}: {e}"
            logger.error(f"[CivicTasks] {msg}")
            results['errors'].append(msg)

        try:
            if auto_register_selective_service(person):
                results['selective_service_registrations'] += 1
        except Exception as e:
            msg = f"Selective Service reg failed for Person #{person.id}: {e}"
            logger.error(f"[CivicTasks] {msg}")
            results['errors'].append(msg)

    logger.info(f"[CivicTasks] Daily check complete: {results}")
    return results


@shared_task(name='apps.civic_tasks.tasks.deregister_selective_service_age_26')
def deregister_selective_service_age_26():
    """
    Runs daily at 00:30 UTC.
    Federal law removes persons from Selective Service rolls at age 26.
    Finds all active registrants turning 26 today and deregisters them.
    """
    today = date.today()
    logger.info(f"[CivicTasks] Running Selective Service age-26 deregistration for {today}")

    from apps.selective_service.models import SelectiveServiceRegistration

    turning_26 = SelectiveServiceRegistration.objects.filter(
        person__date_of_birth__month=today.month,
        person__date_of_birth__day=today.day,
        person__date_of_birth__year=today.year - 26,
        status='ACTIVE',
    )

    count = turning_26.count()
    turning_26.update(status='DEREGISTERED', deregistered_date=today)
    logger.info(f"[CivicTasks] Deregistered {count} Selective Service registrants who turned 26")
    return {'date': str(today), 'deregistered': count}


def auto_register_voter(person):
    from apps.voter_registration.models import VoterRegistration, VoterID
    from apps.voter_registration.serializers import check_eligibility
    import uuid

    if VoterRegistration.objects.filter(person=person).exists():
        return False

    result = check_eligibility(person)
    if not result['eligible']:
        return False

    reg_number = f"VR-{uuid.uuid4().hex[:8].upper()}"
    reg = VoterRegistration.objects.create(
        person=person,
        registration_number=reg_number,
        party_affiliation='UNAFFILIATED',
        state=person.place_of_birth_state or '',
        registration_date=date.today(),
        status='ACTIVE',
    )

    VoterID.objects.create(
        person=person,
        registration=reg,
        voter_id_number=f"VID-{uuid.uuid4().hex[:10].upper()}",
        issue_date=date.today(),
        expiration_date=date.today().replace(year=date.today().year + 4),
        status='ACTIVE',
    )

    logger.info(f"[AutoVoter] Registered Person #{person.id} — {reg_number}")
    return True


def auto_register_selective_service(person):
    from apps.selective_service.models import SelectiveServiceRegistration
    import uuid

    if person.gender != 'MALE':
        return False

    if SelectiveServiceRegistration.objects.filter(person=person).exists():
        return False

    ss_number = f"SS-{uuid.uuid4().hex[:10].upper()}"
    SelectiveServiceRegistration.objects.create(
        person=person,
        registration_number=ss_number,
        registration_date=date.today(),
        registration_method='AUTO_SYSTEM',
        status='ACTIVE',
    )

    logger.info(f"[AutoSS] Registered Person #{person.id} — {ss_number}")
    return True