from django.urls import path
from rest_framework.routers import DefaultRouter

from journey.api.view_sets import *

router = DefaultRouter()
router.register('journey', JourneyViewSet, basename='journey')

urlpatterns = router.urls
