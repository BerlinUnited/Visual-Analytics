from graphene import InputObjectType, String
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q


def apply_generic_filters(model, queryset, filters):
    if not filters:
        return queryset

    query = Q()
    for filter in filters:
        field_name = filter.field
        value = filter.value

        try:
            # Get the Django model field type
            model_field = model._meta.get_field(field_name)
        except FieldDoesNotExist:
            raise ValueError(
                f"Field '{field_name}' does not exist on model '{model.__name__}'"
            )

        # Convert `value` to the correct type based on the model field
        try:
            if value == "null":
                typed_value = None
            else:
                typed_value = model_field.to_python(value)
        except Exception as e:
            raise ValueError(
                f"Invalid value '{value}' for field '{field_name}': {str(e)}"
            )

        # Build the filter
        query &= Q(**{field_name: typed_value})

    return queryset.filter(query)


# test for generic filters
# this is a type that contains a key value pair
class GenericFilterInput(InputObjectType):
    field = String(required=True)
    value = String()
