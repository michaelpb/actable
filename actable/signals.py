from django.db.models.signals import post_init, post_save, m2m_changed

from actable.models import ActableEvent

def post_save_handler(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']
    event = ActableEvent(
        content_object=instance,
        is_creation=created,
    )
    event.save()

def register_all(model_classes):
    for model_class in model_classes:
        post_save.connect(post_save_handler, sender=model_class)

