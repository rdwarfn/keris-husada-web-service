from rest_framework import serializers

from akademik.models import Krs
from akademik.api.jadwal.serializers import JadwalSerializer
from manajemen.api.mahasiswa.serializers import MahasiswaSerializer

class KrsSerializer(serializers.ModelSerializer):
    jadwal = JadwalSerializer(read_only=True)
    # mahasiswa = MahasiswaSerializer(read_only=True)
    class Meta:
        model = Krs
        fields = '__all__'