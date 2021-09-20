# -*- coding: utf-8 -*-
import logging

from django.contrib import admin
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


class AnonymizableAdminMixin(admin.ModelAdmin):
    DISPLAY_ANONYMIZE_PREFIX = "display_anonymized_"

    def is_anonymizable(self):
        if hasattr(self.model, "anonymizable_fields"):
            return True
        else:
            logger.error(
                _(
                    f"anonymizable_fields not set in {self.model}, "
                    f"add anonymizable decorator or register your model with anonymizable.register method"
                )
            )
            raise Exception(
                _(
                    f"anonymizable_fields not set in {self.model}, "
                    f"add anonymizable decorator or register your model with anonymizable.register method"
                )
            )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if self.is_anonymizable():
            readonly_fields = self.add_anonymizable_fields_to_readonly_fields(readonly_fields, self.model.anonymizable_fields)
        return readonly_fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if self.is_anonymizable():
            fieldsets = self.substitute_anonymizable_fields_from_fieldset(fieldsets, self.model.anonymizable_fields)
        return fieldsets

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if self.is_anonymizable():
            list_display = self.add_anonymizable_fields_to_list_display(list_display, self.model.anonymizable_fields)
        return list_display

    @classmethod
    def add_anonymizable_fields_to_list_display(cls, list_display, anonymizable_fields):
        for anonymizable_field in anonymizable_fields:
            list_display = list(list_display)
            if anonymizable_field in list_display:
                list_display[list_display.index(anonymizable_field)] = cls.DISPLAY_ANONYMIZE_PREFIX + anonymizable_field
        return tuple(list_display)

    @classmethod
    def add_anonymizable_fields_to_readonly_fields(cls, readonly_fields, anonymizable_fields):
        for anonymizable_field in anonymizable_fields:
            readonly_fields = list(readonly_fields)
            if cls.DISPLAY_ANONYMIZE_PREFIX + anonymizable_field not in readonly_fields:
                readonly_fields.append(cls.DISPLAY_ANONYMIZE_PREFIX + anonymizable_field)
        return tuple(readonly_fields)

    @classmethod
    def substitute_anonymizable_fields_from_fieldset(cls, fieldsets, anonymizable_fields):
        for fieldset_name, fieldsets_fields in fieldsets:
            fields = list(fieldsets_fields.get("fields", []))
            for idx, item in enumerate(fields):
                if isinstance(item, (tuple, list)):
                    items = list(item)
                    for index, field in enumerate(items):
                        if field in anonymizable_fields:
                            items[index] = cls.DISPLAY_ANONYMIZE_PREFIX + field
                    fields[idx] = tuple(items)
                elif isinstance(item, str):
                    if item in anonymizable_fields:
                        fields[idx] = cls.DISPLAY_ANONYMIZE_PREFIX + item
            fieldsets_fields["fields"] = tuple(fields)
        return fieldsets


