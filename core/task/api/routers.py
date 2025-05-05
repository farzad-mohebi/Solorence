from django.urls import path
from rest_framework.routers import DefaultRouter

from task.api.view_sets import *

router = DefaultRouter()
router.register('task', TaskViewSet, basename='task')
router.register('event', EventViewSet, basename='event')

urlpatterns = router.urls
