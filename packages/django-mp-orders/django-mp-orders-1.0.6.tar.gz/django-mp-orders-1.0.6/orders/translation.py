
from modeltranslation.translator import translator

from orders.models import PaymentMethod, DeliveryMethod, OrderStatus


translator.register(PaymentMethod, fields=['name'])
translator.register(DeliveryMethod, fields=['name'])
translator.register(OrderStatus, fields=['name'])
