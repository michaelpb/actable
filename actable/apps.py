from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured

class ActableConfig(AppConfig):
    name = 'actable'
    def ready(self):
        '''
        Setup ACTABLE_MODELS, which are automatically assigned pre-save hooks
        to hook into the event system.
        '''
        from actable import signals
        from django.conf import settings
        from django.apps import apps
        model_classes = []
        try:
            model_names = settings.ACTABLE_MODELS
        except AttributeError:
            model_names = []

        # Loop through all model names, checking that they implement the
        # required interface, and add them to the list
        for name in model_names:
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

        # Register pre_save hooks for all classes that were specified
        signals.register_all(model_classes)
