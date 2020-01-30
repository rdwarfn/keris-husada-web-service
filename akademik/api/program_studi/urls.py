from django.urls import path
from akademik.api.program_studi.views import ProgramStudiViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'program_studi', ProgramStudiViewSet, basename='program_studi')

urlpatterns = router.urls