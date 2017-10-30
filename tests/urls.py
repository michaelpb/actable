# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from actable.urls import urlpatterns as actable_urls

urlpatterns = [
    url(r'^', include(actable_urls, namespace='actable')),
]
