from rest_framework import viewsets

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from akademik.models import Matakuliah
from akademik.api.matakuliah.serializers import MatakuliahSerializer
from rest_framework import filters

class MatakuliahViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        JWTAuthentication
    )
    permission_classes =(
        DjangoModelPermissions,
        IsAuthenticated
    )
    serializer_class = MatakuliahSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = [
        'kode',
        'nama',
        'sks',
        'semester', 
        'paritas',
        'aktif',
        'jadwal__dosen__nama_lengkap',
        'jadwal__hari',
        'jadwal__jam_mulai',
        'jadwal__ruang_kuliah__kode',
        'jadwal__ruang_kuliah__nama',
    ]

    def get_queryset(self):
        queryset = Matakuliah.objects.all()
        # username = self.request.query_params.get('u', None)
        # if username is not None:
        #     queryset = queryset.filter(username=username)
        return queryset
