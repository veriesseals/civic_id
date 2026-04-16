"""
apps/law_enforcement/serializers.py

MinimalPersonSerializer — privacy-first design.
Returns only the minimum data a law enforcement officer needs.
'photo' was added to allow visual identity confirmation.
All other sensitive fields (SSN, address, maiden name) remain excluded.
"""

from rest_framework import serializers
from .models import VerificationRequest
from apps.persons.models import Person


class MinimalPersonSerializer(serializers.ModelSerializer):
    """
    Fields returned:
      id, first_name, last_name, date_of_birth, citizenship_status, photo
    Every field here is a deliberate privacy decision.
    """
    class Meta:
        model  = Person
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'citizenship_status', 'photo']


class VerificationRequestSerializer(serializers.ModelSerializer):
    """
    Nests MinimalPersonSerializer so person data is embedded in the
    response rather than requiring a second API call.
    NOTE: person_details is only present on the verify (POST) response.
    The history (GET) endpoint returns person as an FK integer only.
    The frontend uses personMap to resolve name/photo for history rows.
    """
    person_details = MinimalPersonSerializer(source='person', read_only=True)

    class Meta:
        model  = VerificationRequest
        fields = ['id', 'requested_by', 'person', 'person_details', 'reason', 'status', 'requested_at']
        read_only_fields = ['id', 'requested_by', 'status', 'requested_at', 'person_details']