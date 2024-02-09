from django.apps import AppConfig


class OrderControllerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order_controller'


    def ready(self):
        import order_controller.signals
