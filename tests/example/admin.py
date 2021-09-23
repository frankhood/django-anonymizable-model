import copy

from django.contrib import admin

from anonymizable_model.admin import AnonymizableAdminMixin
from tests.example.models import ExampleGDPRModel, ExampleGDPRParentModel


@admin.register(ExampleGDPRModel)
class ExampleGDPRModelAdmin(AnonymizableAdminMixin, admin.ModelAdmin):
    list_display = (
        "__str__",
        "first_name",
        "last_name",
        "phone_number",
        "description",
    )

    fieldsets = (
        (None, {"fields": (
            ("first_name", "last_name"),
            ("phone_number", "description"),
        )}),
    )


class ExampleGDPRModelTabularInline(AnonymizableAdminMixin, admin.TabularInline):
    model = ExampleGDPRModel
    fields = ("first_name", "last_name", "phone_number", "description")


class ExampleGDPRModelStackedInline(AnonymizableAdminMixin, admin.StackedInline):
    model = ExampleGDPRModel
    fields = ("first_name", "last_name", "phone_number", "description")


@admin.register(ExampleGDPRParentModel)
class ExampleGDPRParentModelAdmin(admin.ModelAdmin):
    list_display = ("title",)
    fields = ("title",)
    inlines = [ExampleGDPRModelTabularInline, ExampleGDPRModelStackedInline]
