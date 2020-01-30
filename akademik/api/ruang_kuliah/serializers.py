from rest_framework import serializers

from akademik.models import RuangKuliah

class RuangKuliahSerializer(serializers.ModelSerializer):

    class Meta:
        model = RuangKuliah
        fields = '__all__'