from rest_framework import serializers

from .models import NotaModelo

class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaModelo
        fields = '__all__'