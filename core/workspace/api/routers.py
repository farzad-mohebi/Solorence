from django.urls import path
from rest_framework.routers import DefaultRouter

from workspace.api.view_sets import *
from workspace.api.api_views import *

router = DefaultRouter()
router.register('note', NoteViewSet, basename='note')
router.register('template', NoteTemplateViewSet, basename='template')
router.register('noteattachment', NoteAttachmentViewSet, basename='noteattachment')

urlpatterns = router.urls

urlpatterns += [
    # path('google/create-meet/', GoogleMeetCreateView.as_view(), name='google-meet-create'),
    path('google/exchange-code/', ExchangeGoogleTokenApiView.as_view(), name='exchange_code'),
    path('google/create-event/', CreateMeetEventApiView.as_view(), name='create_event'),
]
