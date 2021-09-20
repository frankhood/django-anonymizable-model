from django.contrib import admin

from django_anonymizable_model.admin import AnonymizableAdminMixin
from tests.example.models import ExampleGDPRModel


@admin.register(ExampleGDPRModel)
class ExampleGDPRModelAdmin(AnonymizableAdminMixin, admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "phone_number",
        "description",
    )
    readonly_fields = (
        "first_name",
    )

    fieldsets = (
        (None, {"fields": (
            ("first_name", "last_name"),
            ("phone_number", "description"),
        )}),
    )
