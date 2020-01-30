from django.urls import path
from akademik.api.matakuliah.views import MatakuliahViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'matakuliah', MatakuliahViewSet, basename='matakuliah')

urlpatterns = router.urls