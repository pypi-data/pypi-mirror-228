
from django.apps import apps, AppConfig
from django.utils.translation import gettext_lazy as _


class OrdersConfig(AppConfig):
    name = 'orders'
    verbose_name = _("Orders")

    def ready(self):
        if not apps.is_installed('djmail'):
            raise Exception('`mp-orders` depends on `mp-email`')

        if not apps.is_installed('cart'):
            raise Exception('`mp-orders` depends on `mp-cart`')
