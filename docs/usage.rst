=====
Usage
=====

To use django-anonymizable-model in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'anonymizable_model',
        ...
    )

Add django-anonymizable-model's URL patterns:

.. code-block:: python

    from anonymizable_model import urls as anonymizable_model_urls


    urlpatterns = [
        ...
        url(r'^', include(anonymizable_model_urls)),
        ...
    ]
