from rest_framework import serializers


class CustomSerializer(serializers.ModelSerializer):
    remove_serializer_field_from_view = {}

    def get_fields(self):
        res = super().get_fields()
        view = self.context.get('view')
        if view and self.remove_serializer_field_from_view.get(view.action):
            for field in self.remove_serializer_field_from_view.get(self.context['view'].action):
                if res.get(field):
                    del res[field]
        return res
