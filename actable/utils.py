import json

from django.contrib.contenttypes.models import ContentType

from actable.models import ActableRelation

def get_gfk(instance):
    '''
    Given a model instance, returns a dictionary of the content_type and
    object_id to allow for easy searching
    '''
    content_type = ContentType.objects.get_for_model(instance)
    return {
        'content_type': content_type,
        'object_id': instance.id,
    }

def get_all_json_events(instance):
    return parse_json_list(get_events(instance, 'cached_json'))

def parse_json_list(json_list):
    return [
        dict(
            date=item['date'],
            **(json.loads(item['cached_json']) if item['cached_json'] else {})
        )
        for item in json_list
    ]

class HtmlWrapper(dict):
    def __str__(self):
        return self['cached_html']

def parse_html_list(html_list):
    return [HtmlWrapper(item) for item in html_list]

def get_events(instance, key, start=None, end=None):
    kwargs = get_gfk(instance)
    results = ActableRelation.objects.filter(**kwargs)
    return results.order_by('-date').values(key, 'date')

