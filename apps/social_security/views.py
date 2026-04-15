from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SocialSecurityRecord
from .serializers import SocialSecuritySerializer


class SocialSecurityViewSet(viewsets.ModelViewSet):
    queryset = SocialSecurityRecord.objects.select_related('person', 'issued_by').all()
    serializer_class = SocialSecuritySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(issued_by=self.request.user)