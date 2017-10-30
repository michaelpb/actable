=============================
actable
=============================

.. image:: https://badge.fury.io/py/actable.svg
    :target: https://badge.fury.io/py/actable

.. image:: https://travis-ci.org/michaelpb/actable.svg?branch=master
    :target: https://travis-ci.org/michaelpb/actable

.. image:: https://codecov.io/gh/michaelpb/actable/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/michaelpb/actable

Flexible activity stream for Python Django supporting an arbitrary number of
associated objects and fast denormalized look-ups. Rendering can be fast too,
with in-DB cached HTML and/or context.

The purpose of Actable is to make it easy and unobtrusive to add activity
log-like streams to as many objects in your database as possible, and make
fetching and rendering those simple and fast: a single query without joins,
selecting and ordering only on indexed fields.


Features
--------

Instead of limiting yourself to "Actor, Verb, Object", you can have any number
of relations specified by a dictionary, as such:

.. code-block:: python

    class ProjectBlogPost:
        def get_actable_context(self):
            # 'Alice created Blog Post Title about Project Name, on the topic
            # of Space'
            return {
                'subject': self.user,
                'verb': 'created',
                'object': self,
                'project': self.project,
                'topic': self.topic,
            }

The notable advantage of this is that the event would be accessible from the
user page, the project page, the blog post page, and even the topic page (e.g.,
all related objects are linked).  Since this would normally result in a
complicated and arbitrary JOIN across many tables, the context (and,
optionally, rendered HTML snippets) are cached for each content type, so only a
much simpler query is required.


Quickstart
----------

Install actable::

    pip install actable

Add it to your `INSTALLED_APPS`:

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


Use
---


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in creating this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
