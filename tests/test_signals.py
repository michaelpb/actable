#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_helpers
------------

Tests for `actable` helper functions and classes.
"""
import json

from django.test import SimpleTestCase, TestCase

from actable.apps import check_and_get_actable_models
from actable.signals import post_save_handler
from django.core.exceptions import ImproperlyConfigured
from example.microblog.models import Author
from actable.models import ActableEvent

from actable.utils import get_gfk

class TestActableSettings(SimpleTestCase):
    def test_settings_empty_pagination(self):
        class FauxSettings:
            ACTABLE_MODELS = []
        models = check_and_get_actable_models(FauxSettings)
        self.assertEqual(models, [])

    def test_settings_valid(self):
        class FauxSettings:
            ACTABLE_MODELS = [
                'microblog.MicroPost',
                'microblog.Author',
                'microblog.Follow',
            ]
        models = check_and_get_actable_models(FauxSettings)
        self.assertEqual(len(models), 3)

    def test_settings_invalid_model(self):
        class FauxSettings:
            ACTABLE_MODELS = [
                'microblog.Author',
                'auth.User',
            ]
        with self.assertRaises(ImproperlyConfigured) as cm:
            check_and_get_actable_models(FauxSettings)
        self.assertIn('must implement', str(cm.exception))

class TestActableSignals(TestCase):
    def test_post_save_handler_created(self):
        author = Author.objects.create(
            name='alice',
            bio='alice in wonderland',
        )
        author.save()
        post_save_handler(Author, instance=author, created=True)
        event = ActableEvent.objects.get(**get_gfk(author))
        self.assertEqual(json.loads(event.cached_json), {
            'subject': 'alice',
            'subject_url': '/posts/alice/',
            'verb': 'joined',
        })

    def test_post_save_handler_updated(self):
        author = Author.objects.create(
            name='alice',
            bio='alice in wonderland',
        )
        author.save()

        post_save_handler(Author, instance=author, created=False)
        event = ActableEvent.objects.get(**get_gfk(author))
        self.assertEqual(json.loads(event.cached_json), {
            'subject': 'alice',
            'subject_url': '/posts/alice/',
            'verb': 'updated their profile',
        })
