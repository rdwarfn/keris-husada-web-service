from rest_framework import serializers

from akademik.models import ProgramStudi

class ProgramStudiSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProgramStudi
        fields = '__all__'