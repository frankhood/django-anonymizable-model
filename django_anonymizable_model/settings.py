from django.conf import settings


DJANGO_ANONYMIZE_CAN_ANONYMIZE_DATABASE = getattr(settings, "DJANGO_ANONYMIZE_CAN_ANONYMIZE_DATABASE", False)