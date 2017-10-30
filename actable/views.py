# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
	ActableRelation,
	ActableEvent,
)


class ActableRelationCreateView(CreateView):

    model = ActableRelation


class ActableRelationDeleteView(DeleteView):

    model = ActableRelation


class ActableRelationDetailView(DetailView):

    model = ActableRelation


class ActableRelationUpdateView(UpdateView):

    model = ActableRelation


class ActableRelationListView(ListView):

    model = ActableRelation


class ActableEventCreateView(CreateView):

    model = ActableEvent


class ActableEventDeleteView(DeleteView):

    model = ActableEvent


class ActableEventDetailView(DetailView):

    model = ActableEvent


class ActableEventUpdateView(UpdateView):

    model = ActableEvent


class ActableEventListView(ListView):

    model = ActableEvent

