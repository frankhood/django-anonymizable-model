# -*- coding: utf-8 -*-
import copy
from itertools import chain
import logging
from typing import Any
from django.utils.functional import empty

from django.utils.translation import gettext as _
from django.contrib.admin import helpers

logger = logging.getLogger(__name__)

class AnonymizableAdminMixin:
    DISPLAY_ANONYMIZE_PREFIX = "display_anonymized_"

    def _display_anonymized_string(self, obj):
        if obj and obj.id:
            return _(f"Anonymized Object {obj.id}")
        return _("Anonymized Object")

    def is_anonymizable(self):
        if hasattr(self.model, "anonymizable_fields"):
            return True
        return False

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if self.is_anonymizable() and not request.user.has_perm("example.can_view_anonymized_fields"):
            readonly_fields = copy.deepcopy(readonly_fields)
            readonly_fields = self.add_anonymizable_fields_to_readonly_fields(readonly_fields, self.model.anonymizable_fields)
        return readonly_fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if self.is_anonymizable() and not request.user.has_perm("example.can_view_anonymized_fields"):
            fieldsets = copy.deepcopy(fieldsets)
            fieldsets = self.substitute_anonymizable_fields_from_fieldset(fieldsets, self.model.anonymizable_fields)
        return fieldsets

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if self.is_anonymizable() and not request.user.has_perm("example.can_view_anonymized_fields"):
            list_display = copy.deepcopy(list_display)
            list_display = self.add_anonymizable_fields_to_list_display(list_display, self.model.anonymizable_fields)
        return list_display

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if obj and obj.id and not request.user.has_perm("example.can_view_anonymized_fields") and self.is_anonymizable:
            class ProxyOriginal:
                def __init__(self, original_object) -> None:
                    self.original_object = original_object

                def __str__(self) -> str:
                    if self.original_object and self.original_object.id:
                        return _(f"Anonymized Object {self.original_object.id}")
                    return _("Anonymized Object")

                def __getattr__(self, name: str) -> Any:
                    if not hasattr(ProxyOriginal, name):
                        return getattr(self.original_object, name)
                    return getattr(self, name)
                
            context.update({
                "subtitle": _(f"Anonymized Object {obj.id}"),
                "original": ProxyOriginal(original_object=obj)
            })
        return super().render_change_form(request, context, add, change, form_url, obj)

    # def get_inline_formsets(self, request, formsets, inline_instances, obj=None):
    #     formsets = copy.deepcopy(formsets)
    #     for formset in formsets:
    #         for obj in formset.queryset:
    #             class ProxyOriginal:
    #                 def __init__(self, original_object) -> None:
    #                     self.original_object = original_object

    #                 def __str__(self) -> str:
    #                     if self.original_object and self.original_object.id:
    #                         return _(f"Anonymized Object {self.original_object.id}")
    #                     return _("Anonymized Object")

    #                 def __getattr__(self, name: str) -> Any:
    #                     if not hasattr(ProxyOriginal, name):
    #                         return getattr(self.original_object, name)
    #                     return getattr(self, name)

    #             obj = ProxyOriginal(original_object=obj)

    #     return super().get_inline_formsets(request, formsets, inline_instances, obj=None)

    @classmethod
    def add_anonymizable_fields_to_list_display(cls, list_display, anonymizable_fields):
        for anonymizable_field in anonymizable_fields:
            list_display = list(list_display)
            if "__str__" in list_display:
                list_display[list_display.index("__str__")] = "_display_anonymized_string"
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


