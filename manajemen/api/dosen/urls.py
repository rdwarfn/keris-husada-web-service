from django.urls import path, include
from .views import DosenViewSet, TransaksiDosenViewSet
from rest_framework import routers

router_dosen = routers.SimpleRouter()
router_dosen.register(r'', DosenViewSet, basename='dosen_api')

router_transaksi = routers.SimpleRouter()
router_transaksi.register(r'transaksi', TransaksiDosenViewSet, basename='transaksi_dosen_api')

urlpatterns = [
    path('', include((router_dosen.urls)), name='dosen'),
    path('transaksi/', include((router_transaksi.urls)), name='transaksi'),
]