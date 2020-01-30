from rest_framework import serializers

from akademik.models import NilaiSemester
from akademik.api.krs.serializers import KrsSerializer
from manajemen.api.dosen.serializers import DosenSerializer

class NilaiSerializer(serializers.ModelSerializer):
    krs = KrsSerializer(read_only=True)
    dosen = DosenSerializer(read_only=True)
    dinilai_pada = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    diperbarui_pada = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    class Meta:
        model = NilaiSemester
        fields = '__all__'