from django.urls import path, include
from .views import MahasiswaViewSet, TransaksiMahasiswaViewSet
from rest_framework import routers

router_mahasiswa = routers.SimpleRouter()
router_mahasiswa.register(r'', MahasiswaViewSet, basename='mahasiswa_api')

router_transaksi = routers.SimpleRouter()
router_transaksi.register(r'transaksi', TransaksiMahasiswaViewSet, basename='transaksi_mahasiswa_api')

urlpatterns = [
    path('', include((router_mahasiswa.urls)), name='mahasiswa'),
    path('transaksi/', include((router_transaksi.urls)), name='transaksi'),
]