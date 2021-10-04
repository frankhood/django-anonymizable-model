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
        
        # for m2m fields
        for m2m_field in model_class._meta.local_many_to_many:
            if m2m_field:
                if not m2m_field.db_table and db_label_prefix not in m2m_field.name:
                    m2m_field.db_table = f"{model_class._meta.app_label}_{model_class._meta.model_name}_{m2m_field.name}"
                elif m2m_field.db_table:
                    m2m_field.db_table.replace(db_label_prefix, "")

        if "display_anonymized_FIELD" not in model_class.__dict__:
            setattr(
                model_class,
                "display_anonymized_FIELD",
                display_anonymized_FIELD
            )
        for field in anonymizable_fields:
            model_field = model_class._meta.get_field(field)
            new_field_column_name = db_label_prefix + model_field.column
            model_field.db_column = new_field_column_name
            model_field.column = new_field_column_name
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
                method.short_description = _(model_field.verbose_name)
        return model_class
    return wrap



