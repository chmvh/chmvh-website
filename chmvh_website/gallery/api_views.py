from rest_framework import generics

from gallery import models, serializers


class PatientListCreateView(generics.ListCreateAPIView):
    """View for creating and listing patients"""

    queryset = models.Patient.objects.all()
    serializer_class = serializers.PatientSerializer
