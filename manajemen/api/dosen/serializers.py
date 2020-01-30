from rest_framework import serializers

from manajemen.models import Dosen, TransaksiDosen
# from akademik.api.matakuliah.serializers import MatakuliahSerializer

class DosenSerializer(serializers.ModelSerializer):
    # matakuliah = MatakuliahSerializer(read_only=True)
    # dosen = DosenSerializer(read_only=True, many=True)
    class Meta:
        model = Dosen
        fields = '__all__'



class TransaksiDosenSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransaksiDosen
        fields = '__all__'
