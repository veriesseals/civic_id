from rest_framework import serializers
from .models import SelectiveServiceRegistration


class SelectiveServiceSerializer(serializers.ModelSerializer):
    person_name = serializers.SerializerMethodField()

    class Meta:
        model = SelectiveServiceRegistration
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_person_name(self, obj):
        return f"{obj.person.first_name} {obj.person.last_name or ''}".strip()