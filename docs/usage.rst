=====
Usage
=====

To use actable in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'actable.apps.ActableConfig',
        ...
    )

Add actable's URL patterns:

.. code-block:: python

    from actable import urls as actable_urls


    urlpatterns = [
        ...
        url(r'^', include(actable_urls)),
        ...
    ]
