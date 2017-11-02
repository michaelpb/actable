#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_helpers
------------

Tests for `actable` helper functions and classes.
"""

from django.test import TestCase

from actable.models import ActableEvent, ActableRelation
from actable.apps import check_and_get_actable_models
from django.core.exceptions import ImproperlyConfigured

class TestActableHelpers(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name='alice',
            bio='alice in wonderland',
        )

    def test_settings_empty_pagination(self):
        class FauxSettings:
            ACTABLE_MODELS = []
        models = check_and_get_actable_model(FauxSettings)
        self.assertEqual(models, [])

    def test_settings_invalid(self):
        class FauxSettings:
            pass
        with self.assertRaises(ImproperlyConfigured):
            check_and_get_actable_model(FauxSettings)

    def test_settings_valid(self):
        class FauxSettings:
            ACTABLE_MODELS = [
                'microblog.MicroPost',
                'microblog.Author',
                'microblog.Follow',
            ]
        models = check_and_get_actable_model(FauxSettings)
        self.assertEqual(len(models), 3)

    def test_settings_invalid_model(self):
        class FauxSettings:
            ACTABLE_MODELS = [
                'microblog.Author',
                'auth.User',
            ]
        with self.assertRaises(ImproperlyConfigured) as cm:
            check_and_get_actable_model(FauxSettings)
        self.assertIn('implement get_actable_relations', str(cm.exception))

    def tearDown(self):
        pass
