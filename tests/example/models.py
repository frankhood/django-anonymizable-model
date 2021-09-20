from django.db import models

from django_anonymizable_model.decorators import anonymizable
from tests.example.managers import ExampleGDPRModelManager
from tests.example.querysets import ExampleGDPRModelQuerySet


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

    class Meta:
        """ExampleGDPRModel Meta."""

        verbose_name = "ExampleGDPRModel"
        verbose_name_plural = "ExampleGDPRModels"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
