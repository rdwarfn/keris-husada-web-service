from rest_framework import viewsets

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from akademik.models import Krs
from akademik.api.krs.serializers import KrsSerializer
from rest_framework import filters

class KrsViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        JWTAuthentication
    )
    permission_classes = (
        DjangoModelPermissions,
        IsAuthenticated
    )
    serializer_class = KrsSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = [
        'id',
        'acc_dosen',
        'mahasiswa__nama_lengkap', 
        'mahasiswa__nim',
        'jadwal__hari',
        'jadwal__jam_mulai',
        'jadwal__ruang_kuliah__kode',
        'jadwal__matakuliah__kode', 
        'jadwal__matakuliah__nama',
        'jadwal__matakuliah__sks',
        'jadwal__matakuliah__semester',
        'jadwal__dosen__nidn',
        'jadwal__dosen__nama_lengkap',
    ]

    def get_queryset(self):
        queryset = Krs.objects.all()
        return queryset
