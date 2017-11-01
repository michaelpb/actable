import json

from django.contrib.contenttypes.models import ContentType

from actable.models import ActableRelation

def get_gfk(instance):
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

def get_events(instance, key, start=None, end=None):
    kwargs = get_gfk(instance)
    results = ActableRelation.objects.filter(**kwargs)
    return list(results.order_by('-date').values(key, 'date'))

