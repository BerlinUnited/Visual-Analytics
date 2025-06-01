from django.db.models import Q,BooleanField

def generic_filter(Model,queryset,query_params):
        filters = Q()
        for field in Model._meta.fields:
            param_value = query_params.get(field.name)
            if param_value and isinstance(field, BooleanField):
                    # Convert string to boolean for boolean fields
                    if param_value.lower() in ('true', '1', 'yes'):
                        param_value = True
                    elif param_value.lower() in ('false', '0', 'no'):
                        param_value = False
                    else:
                        continue  # Skip invalid boolean values
            if param_value == "None" or param_value == "null":
                filters &= Q(**{f"{field.name}__isnull": True})
            elif param_value:
                filters &= Q(**{field.name: param_value})
        # apply filters if provided
        return queryset.filter(filters)