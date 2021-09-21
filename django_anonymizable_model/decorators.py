from django.utils.translation import gettext as _


def anonymizable(db_label_prefix="pa_", anonymizable_fields=None):

    def display_anonymized_FIELD(self):
        return "..."

    def wrap(model_class):
        model_class.db_label_prefix = db_label_prefix
        model_class.anonymizable_fields = anonymizable_fields
        new_db_table_name = db_label_prefix + model_class._meta.db_table
        model_class._meta.db_table = new_db_table_name
        model_class._meta.permissions = [
            ("can_view_anonymized_fields", "Can view anonymized fields",)
        ]
        model_class._meta.original_attrs.update({
            "db_table": new_db_table_name
        })
        model_class._meta.original_attrs.update({
            "permissions": [("can_view_anonymized_fields", "Can view anonymized fields",)]
        })
        if "display_anonymized_FIELD" not in model_class.__dict__:
            setattr(
                model_class,
                "display_anonymized_FIELD",
                display_anonymized_FIELD
            )
        for field in anonymizable_fields:
            model_field = getattr(model_class, field)
            new_field_column_name = db_label_prefix + model_field.field.column
            model_field.field.db_column = new_field_column_name
            model_field.field.column = new_field_column_name
            # For Admin visualization
            if 'display_anonymized_%s' % field not in model_class.__dict__:
                def wrapped_display_anonymized_function(self):
                    return self.display_anonymized_FIELD()
                setattr(
                    model_class,
                    'display_anonymized_%s' % field,
                    wrapped_display_anonymized_function,
                )
                method = getattr(model_class, 'display_anonymized_%s' % field)
                method.short_description = _(model_field.field.verbose_name)
        return model_class
    return wrap



