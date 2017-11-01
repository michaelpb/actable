import json

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db import models, transaction

def get_gfk(instance):
    # TODO refactor into shared utils
    content_type = ContentType.objects.get_for_model(instance)
    return {
        'content_type': content_type,
        'object_id': instance.id,
    }


class ActableBase(models.Model):
    class Meta:
        abstract = True
        get_latest_by = '-date'

    # Related object
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    # , db_index=True)
    content_object = GenericForeignKey()

    cached_html = models.TextField(
        help_text='Cached HTML snippet',
        null=True,
        blank=True,
    )

    cached_json = models.TextField(
        help_text='Cached JSON representation of context',
        null=True,
        blank=True,
    )

    date = models.DateTimeField(
        help_text='Date that this event occurred',
        auto_now_add=True,
        db_index=True,
    )

    is_cache_outdated = models.BooleanField(
        help_text='Mark if it is known that this cache needs updating',
        default=False,
    )


class ActableEvent(ActableBase):
    cache_updated_date = models.DateTimeField(
        help_text='Date that the cache of this event was last updated',
        auto_now=True,
    )

    is_creation = models.BooleanField(
        help_text='Mark if this event is the creation of the principle object',
        default=False,
    )

    def save(self, **kwargs):
        relation_context = self.get_relation_context()
        is_new = not self.id
        self.regenerate_cache(relation_context)
        with transaction.atomic():
            super().save()  # Ensure get ID first

            if not is_new:
                # Delete all existing associated
                ActableRelation.objects.filter(event=self).delete()
            self.create_relations_from_self(relation_context)

    def get_principle_object(self):
        return self.content_object

    def rerender_to_cache(self):
        # TODO: Add option to pass in pre-fetched relations since often
        # at least one relation will already be fetched
        relations = ActableRelations.objects.filter(stream_item=self) \
            .select_related('context_object')
        self.render_to_cache(relations)

    def render(self, template_string, relations):
        context = {
            relation.relation: relation.context_object
            for relation in relations
        }

        context['date'] = self.date
        return Template(template_string).render(context)

    def create_relations_from_self(self, relation_context):
        '''
        Given a relation_context dictionary, create in the database all
        relevant relations for this event
        '''
        # Loop through context items
        relations = [
            ActableRelation(
                relation=relation_name,
                cached_html=self.cached_html,
                cached_json=self.cached_json,
                date=self.date,
                event=self,
                **get_gfk(content_object),
            )
            for relation_name, content_object in relation_context.items()
        ]
        ActableRelation.objects.bulk_create(relations)
        print('this is the relations', relations)

    def get_relation_context(self):
        '''
        Gets all related objects to this event
        '''
        return self.content_object.get_actable_relations(self)

    def get_json(self, relation_context):
        if not hasattr(self.content_object, 'get_actable_json'):
            return None
        return self.content_object.get_actable_json(self)

    def get_html(self, relation_context):
        if not hasattr(self.content_object, 'get_actable_html'):
            return None
        return self.content_object.get_actable_html(self)

    def regenerate_cache(self, relation_context):
        self.cached_html = self.get_html(relation_context)
        json_dict = self.get_json(relation_context)
        self.cached_json = json.dumps(json_dict) if json_dict else None

class ActableRelation(ActableBase):
    '''
    Relates a single event to all related objects, storing a copy of the cached
    HTML or JSON snippets for each one.
    '''
    event = models.ForeignKey(ActableEvent)
    relation = models.CharField(
        help_text='Description of grammatical or topical relation (e.g. '
                  '"subject", "target", or "project_context")',
        max_length=64,
        db_index=True,
    )

    def get_principle_object(self):
        return self.event.content_object

    def __str__(self):
        return '%s: %s (%s)' % (self.relation, str(self.content_object), self.date)

