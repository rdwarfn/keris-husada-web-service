from rest_framework import viewsets

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from akademik.models import RuangKuliah
from akademik.api.ruang_kuliah.serializers import RuangKuliahSerializer

class RuangKuliahViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        JWTAuthentication
    )
    permission_classes = (
        DjangoModelPermissions,
        IsAuthenticated
    )
    serializer_class = RuangKuliahSerializer

    def get_queryset(self):
        queryset = RuangKuliah.objects.all()
        return queryset
