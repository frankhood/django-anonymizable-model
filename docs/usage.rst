=====
Usage
=====

To use django-anonimizable-model in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_anonimizable_model.apps.DjangoAnonimizableModelConfig',
        ...
    )

Add django-anonimizable-model's URL patterns:

.. code-block:: python

    from django_anonimizable_model import urls as django_anonimizable_model_urls


    urlpatterns = [
        ...
        url(r'^', include(django_anonimizable_model_urls)),
        ...
    ]
