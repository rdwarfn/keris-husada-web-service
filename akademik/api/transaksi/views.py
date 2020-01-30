from rest_framework import viewsets

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from akademik.models import Transaksi_mahasiswa, Transaksi_dosen
from akademik.api.transaksi.serializers import (
    TransaksiMahasiswaSerializer,
    TransaksiDosenSerializer
)
from rest_framework import filters

class TransaksiMahasiswaViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        JWTAuthentication
    )
    permission_classes = (
        DjangoModelPermissions,
        IsAuthenticated
    )
    serializer_class = TransaksiMahasiswaSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = [
        # 'hari', 
        # 'matakuliah__nama',
        # 'dosen__nama_lengkap',
        # 'dosen__id',
        # 'jam_mulai',
        # 'ruang_kuliah__nama_ruangan',
        # 'ruang_kuliah__kode',
        # 'tampil',
    ]

    def get_queryset(self):
        queryset = Transaksi_mahasiswa.objects.all()
        # dosen = self.request.query_params.get('d', None)
        # if dosen is not None:
        #     '''
        #     return all jadwal spesific dosen
        #     '''
        #     queryset = queryset.filter(dosen__id=dosen)
        return queryset


class TransaksiDosenViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        JWTAuthentication
    )
    permission_classes = (
        DjangoModelPermissions,
        IsAuthenticated
    )
    serializer_class = TransaksiDosenSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = [
        # 'hari', 
        # 'matakuliah__nama',
        # 'dosen__nama_lengkap',
        # 'dosen__id',
        # 'jam_mulai',
        # 'ruang_kuliah__nama_ruangan',
        # 'ruang_kuliah__kode',
        # 'tampil',
    ]

    def get_queryset(self):
        queryset = Transaksi_dosen.objects.all()
        return queryset
