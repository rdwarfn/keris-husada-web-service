from rest_framework import serializers

from akademik.models import Transaksi_mahasiswa, Transaksi_dosen

from mahasiswa.api.serializers import MahasiswaSerializer
from dosen.api.serializers import DosenSerializer

class TransaksiMahasiswaSerializer(serializers.ModelSerializer):
    mahasiswa = MahasiswaSerializer(read_only=True)
    class Meta:
        model = Transaksi_mahasiswa
        fields = '__all__'

class TransaksiDosenSerializer(serializers.ModelSerializer):
    dosen = DosenSerializer(read_only=True)
    class Meta:
        models = Transaksi_dosen
        fields = '__all__'