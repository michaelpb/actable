from actable.models import get_events
from actable.utils import parse_html_list, parse_json_list
from django.core.paginator import Paginator

from django.forms.models import model_to_dict, fields_for_model

class EventHtmlPaginator(Paginator):
    def __init__(self, model_instance, *args, **kwargs):
        queryset = get_events(model_instance, 'cached_html')
        super().__init__(queryset, *args, **kwargs)

    def page(self, *args):
        page = super().page(*args)
        page.object_list = parse_html_list(page.object_list)
        return page


class EventDictPaginator(Paginator):
    def __init__(self, model_instance, *args, **kwargs):
        queryset = get_events(model_instance, 'cached_json')
        super().__init__(queryset, *args, **kwargs)

    def page(self, *args):
        page = super().page(*args)
        page.object_list = parse_json_list(page.object_list)
        return page

class ModelChangeDetector:
    def __init__(self, model_instance):
        self.model_instance = model_instance
        self.freeze_state()

    def freeze_state(self):
        self.editable_fields = set(fields_for_model(self.model_instance).keys())
        self.dict = dict(model_to_dict(self.model_instance))

    def get_changes(self, keys=None):
        current = dict(model_to_dict(self.model_instance))
        if keys is None:
            keys = self.dict.keys()
        return {
            key: (self.dict.get(key), current.get(key)) for key in keys
            if self.dict.get(key) != current.get(key)
        }

    def get_editable_changes(self):
        return self.get_changes(self.editable_fields)


