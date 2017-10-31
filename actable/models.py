from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction

def default_get_actable_relations(obj):
    ctx = {}
    ctx['object'] = obj
    if hasattr(obj, 'author'):
        ctx['subject'] = obj.author
    elif hasattr(obj, 'user'):
        ctx['subject'] = obj.user
    return ctx

class ActableBase(models.Model):
    class Meta:
        abstract = True
        get_latest_by = 'date'

    # Related object
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    topic_object = GenericForeignKey()

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

    def get_principle_object(self):
        return self.topic_object

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
                topic_object=topic_object,
                cached_html=self.cached_html,
                cached_json=self.cached_json,
                date=self.date,
                event=self,
            )
            for relation_name, topic_object in relation_context.items()
        ]
        ActableRelation.objects.bulk_create(relations)

    def get_relation_context(self):
        '''
        Gets the relevant context for the object
        '''
        if hasattr(self.topic_object, 'get_actable_relations'):
            return self.topic_object.get_actable_relations()
        return default_get_actable_relations(self.topic_object)

    def get_json(self, relation_context):
        if not hasattr(self.topic_object, 'get_actable_json'):
            return None
        return self.topic_object.get_actable_json(relation_context)

    def get_html(self, relation_context):
        if not hasattr(self.topic_object, 'get_actable_html'):
            return None
        return self.topic_object.get_actable_html(relation_context)

    def regenerate_cache(self, relation_context):
        self.cached_html = self.get_html(relation_context)
        json_dict = self.get_json(relation_context)
        self.cached_json = json.dumps(json_dict)

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
        return self.event.topic_object

