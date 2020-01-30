from rest_framework import viewsets

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from akademik.models import NilaiSemester
from akademik.api.nilai.serializers import NilaiSerializer
from rest_framework import filters

class NilaiViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        JWTAuthentication
    )
    permission_classes = (
        DjangoModelPermissions,
        IsAuthenticated
    )
    serializer_class = NilaiSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = [
        'krs__status',
        'mahasiswa__nim',
        'krs__mahasiswa__nama_lengkap',
        'krs__jadwal__dosen__nidn',
        'krs__jadwal__dosen__nama_lengkap',
        'krs__jadwal__matakuliah__kode',
        'krs__jadwal__matakuliah__nama',
        'krs__jadwal__matakuliah__sks',
    ]

    def get_queryset(self):
        queryset = NilaiSemester.objects.all()
        return queryset
