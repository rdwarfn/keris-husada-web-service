from rest_framework import serializers

from akademik.models import KHS
from akademik.api.krs.serializers import KrsSerializer
from akademik.api.nilai.serializers import NilaiSerializer

class KhsSerializer(serializers.ModelSerializer):
    krs = KrsSerializer(read_only=True)
    nilai = NilaiSerializer(read_only=True)
    class Meta:
        model = KHS
        fields = '__all__'