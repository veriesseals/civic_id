from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SelectiveServiceRegistration
from .serializers import SelectiveServiceSerializer


class SelectiveServiceViewSet(viewsets.ModelViewSet):
    queryset = SelectiveServiceRegistration.objects.select_related('person', 'registered_by').all()
    serializer_class = SelectiveServiceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(registered_by=self.request.user)