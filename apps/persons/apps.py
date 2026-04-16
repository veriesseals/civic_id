from django.apps import AppConfig


class PersonsConfig(AppConfig):
    name = 'apps.persons'

    def ready(self):
        # Importing the signals module registers all @receiver decorators.
        # This triggers auto_create_id_application whenever a Person is saved.
        import apps.persons.signals  # noqa: F401