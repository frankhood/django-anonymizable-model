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

Add it to your `INSTALLED_APPS`:

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

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
