from rest_framework import serializers

from akademik.models import Jadwal
from akademik.api.matakuliah.serializers import MatakuliahSerializer
from manajemen.api.dosen.serializers import DosenSerializer

class JadwalSerializer(serializers.ModelSerializer):
    matakuliah = MatakuliahSerializer(read_only=True)
    dosen = DosenSerializer(read_only=True, many=True)
    class Meta:
        model = Jadwal
        fields = '__all__'