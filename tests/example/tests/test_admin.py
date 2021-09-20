from django.test import TestCase


# ==============================================
# ./manage.py test tests.example.tests.test_admin.ExampleGDPRModelAdminUnitTest
# ==============================================
class ExampleGDPRModelAdminUnitTest(TestCase):

    def test_substitute_anonymizable_fields_from_fieldset(self):
        # ==============================================
        # ./manage.py test tests.example.tests.test_admin.ExampleGDPRModelAdminUnitTest.test_substitute_anonymizable_fields_from_fieldset
        # ==============================================
        from tests.example.admin import ExampleGDPRModelAdmin
        fieldsets = (
            (None, {"fields": (
                ("first_name",),
                "last_name",
                ("phone_number", "description"),
            )}),
        )
        anonymizable_fields = ["first_name", "last_name", "phone_number"]
        fieldsets = ExampleGDPRModelAdmin.substitute_anonymizable_fields_from_fieldset(fieldsets, anonymizable_fields)
        self.assertEqual(
            fieldsets,
            (
                (None, {'fields': (
                    (f'{ExampleGDPRModelAdmin.DISPLAY_ANONYMIZE_PREFIX}first_name',),
                    f'{ExampleGDPRModelAdmin.DISPLAY_ANONYMIZE_PREFIX}last_name',
                    (f'{ExampleGDPRModelAdmin.DISPLAY_ANONYMIZE_PREFIX}phone_number', 'description')
                )}),
            )
        )

    def test_add_anonymizable_fields_to_readonly_fields(self):
        # ==============================================
        # ./manage.py test tests.example.tests.test_admin.ExampleGDPRModelAdminUnitTest.test_add_anonymizable_fields_to_readonly_fields
        # ==============================================
        from tests.example.admin import ExampleGDPRModelAdmin
        readonly_fields = (
            "created",
            "modified"
        )
        anonymizable_fields = ["first_name", "last_name", "phone_number"]
        readonly_fields = ExampleGDPRModelAdmin.add_anonymizable_fields_to_readonly_fields(readonly_fields, anonymizable_fields)
        self.assertEqual(
            readonly_fields,
            (
                "created",
                "modified",
                f"{ExampleGDPRModelAdmin.DISPLAY_ANONYMIZE_PREFIX}first_name",
                f"{ExampleGDPRModelAdmin.DISPLAY_ANONYMIZE_PREFIX}last_name",
                f"{ExampleGDPRModelAdmin.DISPLAY_ANONYMIZE_PREFIX}phone_number",
            )
        )

    def test_add_anonymizable_fields_to_list_display(self):
        # ==============================================
        # ./manage.py test tests.example.tests.test_admin.ExampleGDPRModelAdminUnitTest.test_add_anonymizable_fields_to_list_display
        # ==============================================
        from tests.example.admin import ExampleGDPRModelAdmin
        list_display = (
            "first_name", "last_name", "phone_number", "description"
        )
        anonymizable_fields = ["first_name", "last_name", "phone_number"]
        list_display = ExampleGDPRModelAdmin.add_anonymizable_fields_to_list_display(list_display, anonymizable_fields)
        self.assertEqual(
            list_display,
            (
                f"{ExampleGDPRModelAdmin.DISPLAY_ANONYMIZE_PREFIX}first_name",
                f"{ExampleGDPRModelAdmin.DISPLAY_ANONYMIZE_PREFIX}last_name",
                f"{ExampleGDPRModelAdmin.DISPLAY_ANONYMIZE_PREFIX}phone_number",
                "description"
            )
        )
