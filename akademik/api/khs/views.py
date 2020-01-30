from rest_framework import viewsets

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from akademik.models import KHS
from akademik.api.khs.serializers import KhsSerializer
from rest_framework import filters

class KhsViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        JWTAuthentication
    )
    permission_classes = (
        DjangoModelPermissions,
        IsAuthenticated
    )
    serializer_class = KhsSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = [
        'krs__mahasiswa__nama_lengkap', 
        'krs__mahasiswa__nim',
        'krs__jadwal__matakuliah__nama',
        'krs__jadwal__matakuliah__semester',
        'krs__jadwal__tahun_akademik',
        'krs__jadwal__matakuliah__paritas', 
    ]

    def get_queryset(self):
        queryset = KHS.objects.all()
        mhs_nim = self.request.query_params.get('n', None)
        thn_akdmk = self.request.query_params.get('a', None)
        smtr = self.request.query_params.get('s', None)

        if (mhs_nim is not None and
            thn_akdmk is not None and
            smtr is not None):
            queryset = queryset.filter(
                krs__mahasiswa__nim=mhs_nim,
                krs__jadwal__tahun_akademik=thn_akdmk,
                krs__jadwal__matakuliah__paritas=smtr
            )
        
        return queryset
