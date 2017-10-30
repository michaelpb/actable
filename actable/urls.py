# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(
        regex="^ActableRelation/~create/$",
        view=views.ActableRelationCreateView.as_view(),
        name='ActableRelation_create',
    ),
    url(
        regex="^ActableRelation/(?P<pk>\d+)/~delete/$",
        view=views.ActableRelationDeleteView.as_view(),
        name='ActableRelation_delete',
    ),
    url(
        regex="^ActableRelation/(?P<pk>\d+)/$",
        view=views.ActableRelationDetailView.as_view(),
        name='ActableRelation_detail',
    ),
    url(
        regex="^ActableRelation/(?P<pk>\d+)/~update/$",
        view=views.ActableRelationUpdateView.as_view(),
        name='ActableRelation_update',
    ),
    url(
        regex="^ActableRelation/$",
        view=views.ActableRelationListView.as_view(),
        name='ActableRelation_list',
    ),
	url(
        regex="^ActableEvent/~create/$",
        view=views.ActableEventCreateView.as_view(),
        name='ActableEvent_create',
    ),
    url(
        regex="^ActableEvent/(?P<pk>\d+)/~delete/$",
        view=views.ActableEventDeleteView.as_view(),
        name='ActableEvent_delete',
    ),
    url(
        regex="^ActableEvent/(?P<pk>\d+)/$",
        view=views.ActableEventDetailView.as_view(),
        name='ActableEvent_detail',
    ),
    url(
        regex="^ActableEvent/(?P<pk>\d+)/~update/$",
        view=views.ActableEventUpdateView.as_view(),
        name='ActableEvent_update',
    ),
    url(
        regex="^ActableEvent/$",
        view=views.ActableEventListView.as_view(),
        name='ActableEvent_list',
    ),
	]
