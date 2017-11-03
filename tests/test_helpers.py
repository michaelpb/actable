#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_helpers
------------

Tests for `actable` helper functions and classes.
"""

from actable.helpers import EventDictPaginator, EventHtmlPaginator
from actable.models import ActableEvent
from django.test import TestCase
from example.microblog.models import Author, MicroPost


class TestActableHelpers(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name='alice',
            bio='alice in wonderland',
        )

    def _strip_dates(self, *lists):
        for lst in lists:
            for item in lst:
                self.assertTrue(bool(item.get('date')))
                del item['date']

    def test_json_pagination(self):
        for x in range(10):
            post = MicroPost.objects.create(
                author=self.author,
                title='title',
                body='body',
            )
            event = ActableEvent(
                content_object=post,
            )
            event.save()
        paginator = EventDictPaginator(self.author, 2)
        self.assertEqual(paginator.count, 10)
        self.assertEqual(paginator.num_pages, 5)
        self.assertEqual(paginator.page_range, range(1, 6))
        page = paginator.page(1)
        self.assertEqual(len(page.object_list), 2)
        self.assertTrue(page.has_next())
        self.assertFalse(page.has_previous())
        items = list(page.object_list)
        self._strip_dates(items)
        self.assertEqual(items, [
            {
                'subject': 'alice',
                'subject_url': '/posts/alice/',
                'object': 'title',
                'object_url': '/post/10/',
                'verb': 'updated',
            },
            {
                'subject': 'alice',
                'subject_url': '/posts/alice/',
                'object': 'title',
                'object_url': '/post/9/',
                'verb': 'updated',
            },
        ])

    def test_html_pagination(self):
        for x in range(10):
            post = MicroPost.objects.create(
                author=self.author,
                title='title',
                body='body',
            )
            event = ActableEvent(
                content_object=post,
            )
            event.save()
        paginator = EventHtmlPaginator(self.author, 3)
        self.assertEqual(paginator.count, 10)
        self.assertEqual(paginator.num_pages, 4)
        self.assertEqual(paginator.page_range, range(1, 5))
        page = paginator.page(1)
        self.assertEqual(len(page.object_list), 3)
        self.assertTrue(page.has_next())
        self.assertFalse(page.has_previous())
        items = list(page.object_list)
        self._strip_dates(items)
        all_htmls = set(map(str, items))
        self.assertEqual(len(all_htmls), 1)
        html = list(all_htmls)[0]
        self.assertEqual(html, '<strong>alice</strong> wrote title')

    def tearDown(self):
        pass
