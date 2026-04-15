from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import MarriageCertificate
from .serializers import MarriageCertificateSerializer


class MarriageCertificateViewSet(viewsets.ModelViewSet):
    queryset = MarriageCertificate.objects.select_related('spouse_1', 'spouse_2', 'filed_by').all()
    serializer_class = MarriageCertificateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(filed_by=self.request.user)