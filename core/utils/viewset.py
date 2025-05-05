from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class CustomModelViewSet(ModelViewSet):
    disable_views = []

    def perform_update(self, serializer):
        if 'update' in self.disable_views:
            raise ValueError('Update function is not offered in this path.', status.HTTP_403_FORBIDDEN)
        super().perform_update(serializer)

    def perform_create(self, serializer):
        if 'create' in self.disable_views:
            raise ValueError('Create function is not offered in this path.', status.HTTP_403_FORBIDDEN)
        super().perform_create(serializer)

    def perform_destroy(self, instance):
        if 'delete' in self.disable_views or 'destroy' in self.disable_views:
            raise ValueError('Delete function is not offered in this path.', status.HTTP_403_FORBIDDEN)
        super().perform_destroy(instance)
