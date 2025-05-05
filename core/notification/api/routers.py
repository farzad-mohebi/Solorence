from django.urls import path
from rest_framework.routers import DefaultRouter

from notification.api.view_sets import *

router = DefaultRouter()
router.register('notification', NotificationViewSet, basename='notification')

urlpatterns = router.urls
