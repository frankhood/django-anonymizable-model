from django.db import models

from anonymizable_model.decorators import anonymizable
from tests.example.managers import ExampleGDPRModelManager, ExampleGDPRParentModelManager
from tests.example.querysets import ExampleGDPRModelQuerySet, ExampleGDPRParentModelQuerySet


@anonymizable(
    db_label_prefix="pa_",
    anonymizable_fields=["first_name", "last_name", "phone_number"]
)
class ExampleGDPRModel(models.Model):
    objects = ExampleGDPRModelManager.from_queryset(ExampleGDPRModelQuerySet)()

    first_name = models.CharField("First name", max_length=255)
    last_name = models.CharField("Last name", max_length=255)
    phone_number = models.CharField("Phone number", max_length=255, blank=True, default="")
    description = models.TextField("Description", blank=True, default="")
    parent = models.ForeignKey(
        "example.ExampleGDPRParentModel",
        blank=True, null=True, default=None,
        related_name="example_gdprs",
        on_delete=models.CASCADE)

    class Meta:
        """ExampleGDPRModel Meta."""

        verbose_name = "ExampleGDPRModel"
        verbose_name_plural = "ExampleGDPRModels"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ExampleGDPRParentModel(models.Model):
    objects = ExampleGDPRParentModelManager.from_queryset(ExampleGDPRParentModelQuerySet)()

    title = models.CharField("Title", max_length=255)

    class Meta:
        """Example GDPR Parent Model Meta."""

        verbose_name = "Example GDPR Parent Model"
        verbose_name_plural = "Example GDPR Parent Models"

    def __str__(self):
        return self.title



