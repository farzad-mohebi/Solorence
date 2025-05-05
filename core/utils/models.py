from copy import deepcopy


class CustomModel:

    @classmethod
    def serializer_fields(cls, excludes=None) -> list:
        # Returns a list of all Model fields
        fields = [field.attname.replace('_id', '') for field in cls._meta.fields]
        many_2_many = [m2m_field.name for m2m_field in cls._meta.many_to_many]
        all_fields = fields + many_2_many
        result = list(deepcopy(all_fields))
        if excludes:
            result = [field for field in result if field not in excludes]
        return result

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)
