from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

class ActableBase(models.model):
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
    )

    cache_updated_date = models.DateTimeField(
        help_text='Date that the cache of this event was last updated',
        auto_add=True,
    )


class ActableRelation(ActableBase):
    event = models.ForeignKey(ActableEvent)
    relation = models.CharField(
        help_text='Description of grammatical or topical relation (e.g. '
                  '"subject", "target", or "project_context")',
        max_length=64,
        db_index=True,
    )

    def get_principle_object(self):
        return self.event.topic_object


class ActableEvent(models.Model):
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

    @classmethod
    def new_from_obj(cls, obj):
        if hasattr(obj, 'get_actable_related_objects'):
            ctx = obj.get_actable_related_objects()

        with transaction:
            event = ActableEvent(
                content_type=get_context_type(obj),
                context_object=obj,
            )

        return event
