from django.core.paginator import Paginator, Page

from actable.utils import get_events, parse_json_list, parse_html_list

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


