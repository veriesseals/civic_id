from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Passport
from .serializers import PassportSerializer


class PassportViewSet(viewsets.ModelViewSet):
    queryset           = Passport.objects.select_related("person", "issued_by").all()
    serializer_class   = PassportSerializer
    permission_classes = [IsAuthenticated]
