from rest_framework import serializers

from akademik.models import Absensi

from akademik.api.jadwal.serializers import JadwalSerializer
from manajemen.api.mahasiswa.serializers import MahasiswaSerializer

class AbsensiSerializer(serializers.ModelSerializer):
    mahasiswa = MahasiswaSerializer(read_only=True)
    jadwal = JadwalSerializer(read_only=True)
    class Meta:
        model = Absensi
        fields = '__all__'