from rest_framework import viewsets
from rest_framework import generics

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions


from akademik.models import ProgramStudi
from akademik.api.program_studi.serializers import ProgramStudiSerializer
from rest_framework import filters

class ProgramStudiViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes  = (DjangoModelPermissions, IsAuthenticated)
    serializer_class    = ProgramStudiSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = [
        'nama',
        'singkat',
        'akreditasi',
    ]

    def get_queryset(self):
        queryset = ProgramStudi.objects.all()
        username = self.request.query_params.get('u', None)
        if username is not None:
            queryset = queryset.filter(username=username)
        return queryset
