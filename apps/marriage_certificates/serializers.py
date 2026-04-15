from rest_framework import serializers
from .models import MarriageCertificate


class MarriageCertificateSerializer(serializers.ModelSerializer):
    spouse_1_name = serializers.SerializerMethodField()
    spouse_2_name = serializers.SerializerMethodField()

    class Meta:
        model = MarriageCertificate
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_spouse_1_name(self, obj):
        return f"{obj.spouse_1.first_name} {obj.spouse_1.last_name or ''}".strip()

    def get_spouse_2_name(self, obj):
        return f"{obj.spouse_2.first_name} {obj.spouse_2.last_name or ''}".strip()