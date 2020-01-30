from rest_framework import viewsets
from rest_framework import filters
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
# from django_rest_passwordreset.signals import reset_password_token_created
from manajemen.models import Mahasiswa, TransaksiMahasiswa
from .serializers import MahasiswaSerializer, TransaksiMahasiswaSerializer

class MahasiswaViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes  = (DjangoModelPermissions, IsAuthenticated)
    serializer_class    = MahasiswaSerializer
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = [
        'nama_lengkap',
        'akun__id',
        'akun__username',
    ]

    def get_queryset(self):
        queryset = Mahasiswa.objects.all()
        return queryset


class TransaksiMahasiswaViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionAuthentication, 
        JWTAuthentication,
    )
    permission_classes = (
        DjangoModelPermissions,
        IsAuthenticated,
    )
    serializer_class = TransaksiMahasiswaSerializer
    parser_classes = (
        JSONParser,
        FormParser,
        MultiPartParser,
    )

    def get_queryset(self):
        queryset = TransaksiMahasiswa.objects.all()
        return queryset