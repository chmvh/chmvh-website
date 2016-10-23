from rest_framework import serializers

from gallery import models


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'picture': {
                'write_only': True,
            },
        }
        fields = ('first_name', 'last_name', 'featured', 'deceased', 'picture')
        model = models.Patient
