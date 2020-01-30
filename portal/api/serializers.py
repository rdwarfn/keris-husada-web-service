from rest_framework import serializers
from portal.models import *


class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = '__all__'


class SubArtikelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubArtikel
        fields = '___all___'


class ArtikelSerializer(serializers.ModelSerializer):
    kategori = KategoriSerializer(read_only=True)
    sub_artikel = SubArtikelSerializer(read_only=True)
    class Meta:
        model = Artikel
        fields = '__all__'
