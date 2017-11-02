#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_actable
------------

Tests for `actable` models module.
"""
import json

from django.test import TestCase

from actable.models import ActableEvent, ActableRelation
from actable.helpers import EventDictPaginator
from example.microblog.models import Author, Follow, MicroPost

class TestActableModels(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name='alice',
            bio='alice in wonderland',
        )
        self.author2 = Author.objects.create(
            name='bob',
            bio='bob in landwonder',
        )

    def test_singular_relations(self):
        event = ActableEvent(
            content_object=self.author,
        )
        self.assertEqual(len(ActableEvent.objects.all()), 0)
        self.assertEqual(len(ActableRelation.objects.all()), 0)
        event.save()
        self.assertEqual(len(ActableEvent.objects.all()), 1)
        self.assertEqual(len(ActableRelation.objects.all()), 1)

    def test_multiple_relations(self):
        follow = Follow.objects.create(
            author=self.author,
            follower=self.author2,
        )
        event = ActableEvent(
            content_object=follow,
        )
        self.assertEqual(len(ActableEvent.objects.all()), 0)
        self.assertEqual(len(ActableRelation.objects.all()), 0)
        event.save()
        self.assertEqual(len(ActableEvent.objects.all()), 1)
        self.assertEqual(len(ActableRelation.objects.all()), 2)

    def test_different_relation_types(self):
        post = MicroPost.objects.create(
            author=self.author,
            title='title',
            body='body',
        )
        event = ActableEvent(
            content_object=post,
        )
        self.assertEqual(len(ActableEvent.objects.all()), 0)
        self.assertEqual(len(ActableRelation.objects.all()), 0)
        event.save()
        self.assertEqual(len(ActableEvent.objects.all()), 1)
        self.assertEqual(len(ActableRelation.objects.all()), 2)

        # Check JSON
        all_jsons = set([
            act.cached_json for act in list(ActableRelation.objects.all()) +
                list(ActableEvent.objects.all())
        ])
        self.assertEqual(len(all_jsons), 1)
        json_parsed = json.loads(list(all_jsons)[0])
        expected_json = {
            'subject': 'alice',
            'subject_url': '/posts/alice/',
            'object': 'title',
            'object_url': '/post/1/',
            'verb': 'updated',
        }
        self.assertEqual(json_parsed, expected_json)

        # Check HTML
        all_htmls = set([
            act.cached_html for act in list(ActableRelation.objects.all()) +
                list(ActableEvent.objects.all())
        ])
        self.assertEqual(len(all_htmls), 1)
        html = list(all_htmls)[0]
        self.assertEqual(html, '<strong>alice</strong> wrote title')

    def tearDown(self):
        pass

