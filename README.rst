=============================
django-anonimizable-model
=============================

.. image:: https://badge.fury.io/py/django-anonimizable-model.svg
    :target: https://badge.fury.io/py/django-anonimizable-model

.. image:: https://travis-ci.org/frankhood/django-anonimizable-model.svg?branch=master
    :target: https://travis-ci.org/frankhood/django-anonimizable-model

.. image:: https://codecov.io/gh/frankhood/django-anonimizable-model/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/frankhood/django-anonimizable-model

Your project description goes here

Documentation
-------------

The full documentation is at https://django-anonimizable-model.readthedocs.io.

Quickstart
----------

Install django-anonimizable-model::

    pip install django-anonimizable-model

Add it to your `INSTALLED_APPS`::

    INSTALLED_APPS = (
        ...
        'django_anonimizable_model',
        ...
    )

Use on your models like this::

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

It is possible to change db_label_prefix with your own label
and assign anonymizable fields from the model for export and visualization features.

And then run migrations::

    $ python manage.py makemigrations
    $ python manage.py migrate

For the admin visualization use AnonymizableAdminMixin class::

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

The admin can view all anonymized data in fields. If a staff user does not have can_view_anonymized_fields permission
all the data in anonymizable_fields will be substituted with "...".



Features
--------

* Remove or override __str__ method to display "..." if user does not have permission

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python manage.py test tests.example


Development commands
---------------------

::

    pip install -r requirements_dev.txt


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
