from rest_framework import serializers

from manajemen.models import Mahasiswa, TransaksiMahasiswa

class MahasiswaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mahasiswa
        fields = '__all__'


class TransaksiMahasiswaSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransaksiMahasiswa
        fields = '__all__'
