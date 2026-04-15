from rest_framework import serializers
from .models import SocialSecurityRecord


class SocialSecuritySerializer(serializers.ModelSerializer):
    person_name = serializers.SerializerMethodField()
    ssn_display = serializers.SerializerMethodField()

    class Meta:
        model = SocialSecurityRecord
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
        # ssn is write-only — never returned in responses
        extra_kwargs = {'ssn': {'write_only': True}}

    def get_person_name(self, obj):
        return f"{obj.person.first_name} {obj.person.last_name or ''}".strip()

    def get_ssn_display(self, obj):
        return obj.masked_ssn