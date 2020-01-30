from django.urls import path
from portal.api.views import ArtikelViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', ArtikelViewSet, basename='artikel')

urlpatterns = router.urls