from rest_framework import viewsets
from rest_framework import filters
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from manajemen.models import Dosen, TransaksiDosen
from .serializers import DosenSerializer, TransaksiDosenSerializer

class DosenViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes  = (DjangoModelPermissions, IsAuthenticated)
    serializer_class    = DosenSerializer
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
        queryset = Dosen.objects.all()
        return queryset


class TransaksiDosenViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionAuthentication, 
        JWTAuthentication,
    )
    permission_classes = (
        DjangoModelPermissions,
        IsAuthenticated,
    )
    serializer_class = TransaksiDosenSerializer
    parser_classes = (
        JSONParser,
        FormParser,
        MultiPartParser,
    )

    def get_queryset(self):
        queryset = TransaksiDosen.objects.all()
        return queryset