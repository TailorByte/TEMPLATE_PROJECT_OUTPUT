from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users_app'
    verbose_name = 'User Management'

    def ready(self):
        # Import signals here if you have any for this app
        # Example:
        # import users_app.signals
        pass