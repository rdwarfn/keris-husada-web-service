from django.urls import path
from rest_framework import routers
from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r'', UserViewSet, basename='user_api')

urlpatterns = router.urls