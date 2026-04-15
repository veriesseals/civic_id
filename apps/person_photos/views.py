from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import PersonPhoto
from .serializers import PersonPhotoSerializer


class PersonPhotoViewSet(viewsets.ModelViewSet):
    queryset = PersonPhoto.objects.select_related('person', 'uploaded_by').all()
    serializer_class = PersonPhotoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)