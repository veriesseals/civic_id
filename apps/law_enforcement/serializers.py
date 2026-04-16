"""
apps/law_enforcement/serializers.py

MinimalPersonSerializer — privacy-first design.
Only exposes the minimum data a law enforcement officer needs.

UPDATED: Added 'photo' to the fields list so the officer can see
a visual confirmation of identity alongside the name/DOB/citizenship.
The photo field returns a relative URL (e.g. /media/person_photos/x.jpg)
which the frontend resolves to a full URL using the MEDIA_URL setting.

All other sensitive fields (SSN, address, maiden name, etc.) remain
deliberately excluded.
"""

from rest_framework import serializers
from .models import VerificationRequest
from apps.persons.models import Person


class MinimalPersonSerializer(serializers.ModelSerializer):
    """
    Returns only the 6 minimum-necessary fields for a law enforcement
    identity verification. Every field added here is a deliberate
    privacy decision that should be documented.

    Fields returned:
      id               — needed to cross-reference records
      first_name       — identity confirmation
      last_name        — identity confirmation
      date_of_birth    — identity confirmation
      citizenship_status — relevant to LE operations
      photo            — visual identity confirmation (NEW)
    """

    class Meta:
        model  = Person
        fields = [
            'id',
            'first_name',
            'last_name',
            'date_of_birth',
            'citizenship_status',
            'photo',           # Added — visual identity confirmation
        ]


class VerificationRequestSerializer(serializers.ModelSerializer):
    """
    Handles the incoming POST from the officer and the outgoing response.
    Nests MinimalPersonSerializer so person data is embedded in the
    response rather than requiring a second API call.
    """

    # Nested read-only person data — populated from the 'person' FK
    person_details = MinimalPersonSerializer(
        source   = 'person',
        read_only = True,
    )

    class Meta:
        model  = VerificationRequest
        fields = [
            'id',
            'requested_by',
            'person',
            'person_details',   # Nested: includes photo now
            'reason',
            'status',
            'requested_at',
        ]

        # These are set automatically by the view — officers cannot spoof them
        read_only_fields = [
            'id',
            'requested_by',
            'status',
            'requested_at',
            'person_details',
        ]