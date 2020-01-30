from rest_framework import viewsets

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from akademik.models import Jadwal
from akademik.api.jadwal.serializers import JadwalSerializer
from rest_framework import filters

class JadwalViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        JWTAuthentication
    )
    permission_classes = (
        DjangoModelPermissions,
        IsAuthenticated
    )
    serializer_class = JadwalSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = [
        'hari', 
        'matakuliah__nama',
        'krs__mahasiswa__nim',
        'dosen__nama_lengkap',
        'dosen__nidn',
        'jam_mulai',
        'ruang_kuliah__nama_ruangan',
        'ruang_kuliah__kode',
        'tampil',
    ]

    def get_queryset(self):
        queryset = Jadwal.objects.all()
        # dosen = self.request.query_params.get('d', None)
        # if dosen is not None:
        #     '''
        #     return all jadwal spesific dosen
        #     '''
        #     queryset = queryset.filter(dosen__id=dosen)
        return queryset
