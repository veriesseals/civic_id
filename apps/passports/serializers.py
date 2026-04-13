from rest_framework import serializers
from .models import Passport
from datetime import date


class PassportSerializer(serializers.ModelSerializer):
    person_name    = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model  = Passport
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def get_person_name(self, obj):
        return f"{obj.person.first_name} {obj.person.last_name or " "}".strip()

    def get_days_remaining(self, obj):
        if not obj.expiration_date:
            return None
        return (obj.expiration_date - date.today()).days
