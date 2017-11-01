from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured

class ActableConfig(AppConfig):
    name = 'actable'
    def ready(self):
        from actable import signals
        from django.conf import settings
        from django.apps import apps
        model_classes = []
        for name in settings.ACTABLE_MODELS:
            app_name, _, model_name = name.partition('.')
            model_class = apps.get_model(app_name, model_name)

            if hasattr(model_class, 'get_actable_context'):
                raise ImproperlyConfigured('Invalid ACTABLE_MODELS, must '
                    'implement get_actable_relations method: %s' % name)

            if not (hasattr(model_class, 'get_actable_json') or
                    hasattr(model_class, 'get_actable_html')):
                raise ImproperlyConfigured('Invalid ACTABLE_MODELS, must '
                    'implement either JSON or HTML cache method: %s' % name)
            model_classes.append(model_class)
        signals.register_all(model_classes)
