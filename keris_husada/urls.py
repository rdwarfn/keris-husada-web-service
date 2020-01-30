from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.urls import path, include
# akademik
from akademik.api.program_studi.views import ProgramStudiViewSet
from akademik.api.matakuliah.views import MatakuliahViewSet
from akademik.api.ruang_kuliah.views import RuangKuliahViewSet
from akademik.api.jadwal.views import JadwalViewSet
from akademik.api.krs.views import KrsViewSet
from akademik.api.nilai.views import NilaiViewSet
from akademik.api.absensi.views import AbsensiViewSet
# manajemen
from manajemen.api.user.views import UserViewSet
from manajemen.api.mahasiswa.views import MahasiswaViewSet
# api
from keris_husada.api.views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework import routers

akademi_router = routers.SimpleRouter()
akademi_router.register(r'program_studi', ProgramStudiViewSet, basename='program_studi')
akademi_router.register(r'matakuliah', MatakuliahViewSet, basename='matakuliah')
akademi_router.register(r'ruang_kuliah', RuangKuliahViewSet, basename='ruang_kuliah')
akademi_router.register(r'jadwal', JadwalViewSet, basename='jadwal')
akademi_router.register(r'krs', KrsViewSet, basename='krs')
akademi_router.register(r'nilai', NilaiViewSet, basename='nilai')
akademi_router.register(r'absensi', AbsensiViewSet, basename='absensi')

urlpatterns = [
    path('api/v1/', include([
        path('akademik/', include((akademi_router.urls, 'akademik'), namespace='akademik_api')),
        path('user/', include('manajemen.api.user.urls')),
        path('mahasiswa/', include('manajemen.api.mahasiswa.urls')),
        path('dosen/', include('manajemen.api.dosen.urls')),
        path('portal/', include('portal.api.urls')),
        path('token/', include([
            path('', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
            path('verify/', TokenVerifyView.as_view(), name='token_verify'),
        ])),
    ])),
    path('summernote/', include('django_summernote.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = format_html("{}",
    'Administrasi Akademi Keperawatan',
)
admin.site.site_title = "Sistem Informasi Akademik"
