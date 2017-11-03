# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from actable.urls import urlpatterns as actable_urls
from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include(actable_urls, namespace='actable')),
]
