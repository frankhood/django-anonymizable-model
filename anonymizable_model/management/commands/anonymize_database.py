"""
Anonymise all personal data in the database
"""
from django.core.management import BaseCommand
from anonymizable_model import settings as app_settings


def get_anonymized_models():
    from django.apps import apps
    anonymized_models = []
    for app in apps.get_app_configs():
        for model in app.get_models():
            if hasattr(model, "db_label_prefix") and hasattr(model, "anonymizable_fields"):
                anonymized_models.append(model)
    return anonymized_models


class Command(BaseCommand):
    help = "Anonymises all personal data in the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_false",
            dest="interactive",
            default=True,
            help="Tells Django to NOT prompt the user for input of any kind.",
        )

    def handle(self, *args, **options):
        if not app_settings.DJANGO_ANONYMIZE_CAN_ANONYMIZE_DATABASE:
            raise ValueError("Database anonymisation is not enabled")
        interactive = options["interactive"]

        if interactive:  # pragma: no cover
            confirm = input(
                """Warning!
                You have requested that all personal information in the database is anonymised.
                This will IRREVERSIBLY OVERWRITE all personal data currently in the database.
                Are you sure you want to do this?
                Type 'yes' to continue, or 'no' to cancel: """
            )
        else:
            confirm = "yes"

        if confirm == "yes":
            msg = ""
            for model in get_anonymized_models():
                def anonymize_field(obj, field):
                    display_method = getattr(obj, "display_anonymized_"+ field)
                    setattr(obj, field, display_method())
                    obj.save(update_fields=[field])

                [[anonymize_field(obj, field) for field in model.anonymizable_fields] for obj in model.objects.all()]
                msg += "{} model anonymized. \n".format(model._meta.verbose_name)
            self.stdout.write(msg)

        else:  # pragma: no cover
            self.stdout.write("Anonymisation cancelled.")