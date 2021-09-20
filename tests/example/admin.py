import copy

from django.contrib import admin

from django_anonymizable_model.admin import AnonymizableAdminMixin
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

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        return super().render_change_form(request, context, add, change, form_url, obj)


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
