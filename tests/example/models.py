from django.db import models

from anonymizable_model.decorators import anonymizable
from tests.example.managers import ExampleGDPRModelManager, ExampleGDPRParentModelManager, M2MExampleModelManager
from tests.example.querysets import ExampleGDPRModelQuerySet, ExampleGDPRParentModelQuerySet, M2MExampleModelQuerySet


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
        on_delete=models.CASCADE
    )
    m2m_testing_model = models.ManyToManyField(
        "example.M2MExampleModel",
        verbose_name="m2m_testing_model",
        related_name="examplegdprmodels",
        db_table="example_examplegdprmodel_m2mtestingmodel",
    )

    class Meta:
        """ExampleGDPRModel Meta."""

        verbose_name = "ExampleGDPRModel"
        verbose_name_plural = "ExampleGDPRModels"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class M2MExampleModel(models.Model):
    objects = M2MExampleModelManager.from_queryset(M2MExampleModelQuerySet)()

    subtitle = models.CharField("Subtitle", max_length=255, blank=True, default="")

    class Meta:
        """M2MExampleModel Meta."""

        verbose_name = "M2MExampleModel"
        verbose_name_plural = "M2MExampleModels"


class ExampleGDPRParentModel(models.Model):
    objects = ExampleGDPRParentModelManager.from_queryset(ExampleGDPRParentModelQuerySet)()

    title = models.CharField("Title", max_length=255)

    class Meta:
        """Example GDPR Parent Model Meta."""

        verbose_name = "Example GDPR Parent Model"
        verbose_name_plural = "Example GDPR Parent Models"

    def __str__(self):
        return self.title



