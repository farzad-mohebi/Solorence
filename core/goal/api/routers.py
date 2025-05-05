from django.urls import path
from rest_framework.routers import DefaultRouter

from goal.api.view_sets import *

router = DefaultRouter()
router.register('goal', GoalViewSet, basename='goal')
router.register('goaltarget', GoalTargetViewSet, basename='goaltarget')

urlpatterns = router.urls
