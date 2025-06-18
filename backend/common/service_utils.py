from django.utils import timezone


def update_model(instance, data, auto_updated_at=True):
    has_updated = False
    fields = list(data.keys())
    model_fields = {field.name: field for field in instance._meta.get_fields()}
    updated_fields = []

    for field in fields:
        if field not in data:
            continue

        model_field = model_fields.get(field)
        assert model_field is not None, (
            f"{field} is not part of {instance.__class__.__name__} fields."
        )

        if getattr(instance, field) != data[field]:
            has_updated = True
            updated_fields.append(field)
            setattr(instance, field, data[field])

    if has_updated:
        if auto_updated_at:
            update_updated_at(model_fields, updated_fields, instance)

        instance.full_clean()
        instance.save(update_fields=updated_fields)

    return instance, has_updated


def update_updated_at(model_fields, updated_fields, instance):
    # We want to take care of the `updated_at` field,
    # Only if the models has that field
    # And if no value for updated_at has been provided
    if "updated_at" in model_fields and "updated_at" not in updated_fields:
        updated_fields.append("updated_at")
        instance.updated_at = timezone.now()  # type: ignore
