=============================
Django Actable
=============================

.. image:: https://img.shields.io/pypi/v/actable.svg
    :target: https://pypi.python.org/pypi/actable/

.. image:: https://travis-ci.org/michaelpb/actable.svg?branch=master
    :target: https://travis-ci.org/michaelpb/actable

.. image:: https://codecov.io/gh/michaelpb/actable/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/michaelpb/actable

* **NOTE:** Presently *only* supports Python 3.5+ and Django 1.9+ (see `issue
  #1 <https://github.com/michaelpb/actable/issues/1>`_)

Activity stream for Python Django. Unlike other activity streams, it is much
more flexible, with every event designed to supporting an arbitrary number of
associated objects. It also is designed to be unobtrusive: Any of your models
can be registered as an activity generator, all you need to do is generate a
data structure for context, or an HTML fragment.

Features
--------

- Very easily / magically integrated into an existing system, with signals
  being auto-generated based on principle objects
- Arbitrary number of objects can be associated with every event
- Fast look ups with denormalized events (no joins)
- Looking up streams for particular actors or objects
- Decent test coverage
- Handy Paginator helper class to page through stream
- Example project

- **Not yet implemented:** Follow


Quick start
------------

**Overview:**

1. Install actable and put in requirements file

2. Add to INSTALLED_APPS

3. Pick several important models to implement the actable interface so that
every save or update generates an event

4. Add those models to ACTABLE_MODELS

5. Use helper classes to add a streams to your views

---------------

Install:

.. code-block:: bash

    pip install actable


Add it to your `INSTALLED_APPS`:


.. code-block:: python

    INSTALLED_APPS = (
        ...
        'actable.apps.ActableConfig',
        ...
    )

Pick one or more models to be your actable models. Whenever these models are
updated or created, it will generate events. These events can involve any
number of other objects.

You must implement at least 2 methods on your actable models. The first method
is ``get_actable_relations`` which must return a dictionary where all the
values are model instances that are related to this action.  Instead of
limiting yourself to "Actor, Verb, Object", this allows you to have any number
of relations.  Each one of these model instances will receive a copy of this
event to its activity stream.

Example:

.. code-block:: python

    class ProjectBlogPost:
        def get_actable_relations(self, event):
            return {
                'subject': self.user,
                'object': self,
                'project': self.project,
            }

Now you must choose one of 2 other methods to implement. These constitute the
data to cache for each event.

The most versatile of the two is one that returns a dictionary containing
entirely simple (serializable) data types. This will be stored in serialized
form in your database.

Example:

.. code-block:: python

    class ProjectBlogPost:
        def get_actable_json(self, event):
            verb = 'posted' if event.is_creation else 'updated'
            return {
                'subject': self.user.username,
                'subject_url': self.user.get_absolute_url(),
                'object': self.title,
                'object_url': self.get_absolute_url(),
                'project': self.project.title,
                'verb': verb,
            }


The other option is caching an HTML snippet (string) that can be generated any
way you see fit.

Example:

.. code-block:: python

    class ProjectBlogPost:
        def get_actable_html(self, event):
            return '<a href="%s">%s</a> wrote %s' % (
                self.user.get_absolute_url(),
                self.user.username,
                self.title
            )

Finally, you should list your newly improved as an ``ACTABLE_MODEL``, as such:

.. code-block:: python

    ACTABLE_MODELS = [
        'myapp.ProjectBlogPost',
    ]


Credits
-------

Tools used in creating this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
