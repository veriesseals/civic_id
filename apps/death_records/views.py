from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import DeathRecord
from .serializers import DeathRecordSerializer


class DeathRecordViewSet(viewsets.ModelViewSet):
    queryset = DeathRecord.objects.select_related('person', 'filed_by').all()
    serializer_class = DeathRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(filed_by=self.request.user)