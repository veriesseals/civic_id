from rest_framework import serializers
from .models import PersonPhoto


class PersonPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonPhoto
        fields = '__all__'
        read_only_fields = ['uploaded_at']