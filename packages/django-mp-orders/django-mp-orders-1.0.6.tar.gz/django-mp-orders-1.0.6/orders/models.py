
from django.apps import apps
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from orders.constants import PAYMENT_METHOD_PRIVAT24


def _generate_hash():
    return get_random_string(length=10)


class OrderStatus(models.Model):

    id = models.CharField(primary_key=True, max_length=100)

    name = models.CharField(_('Name'), max_length=255)

    is_default = models.BooleanField(_("Default"), default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')


class PaymentMethod(models.Model):

    id = models.CharField(primary_key=True, max_length=100)

    name = models.CharField(_('Name'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Payment method')
        verbose_name_plural = _('Payment methods')


class DeliveryMethod(models.Model):

    id = models.CharField(primary_key=True, max_length=100)

    name = models.CharField(_('Name'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Delivery method')
        verbose_name_plural = _('Delivery methods')


class Order(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        related_name='orders',
        verbose_name=_('Owner'),
        null=True,
        blank=True
    )

    status = models.ForeignKey(
        OrderStatus,
        models.CASCADE,
        verbose_name=_('Status')
    )

    payment_method = models.ForeignKey(
        PaymentMethod,
        models.CASCADE,
        verbose_name=_('Payment method'),
    )

    delivery_method = models.ForeignKey(
        DeliveryMethod,
        models.CASCADE,
        verbose_name=_('Delivery method'),
    )

    first_name = models.CharField(_('First name'), max_length=255)

    last_name = models.CharField(_('Last name'), max_length=255)

    middle_name = models.CharField(
        _('Middle name'), max_length=255, blank=True)

    address = models.CharField(_('Address'), max_length=255, blank=True)

    mobile = models.CharField(_('Mobile number'), max_length=255)

    created = models.DateTimeField(
        _('Date created'), auto_now_add=True, editable=False)

    comment = models.TextField(_('Comment'), max_length=1000, blank=True)

    decline_reason = models.TextField(
        _('Decline reason'), max_length=1000, blank=True)

    hash = models.CharField(
        max_length=10,
        default=_generate_hash,
        unique=True)

    def __str__(self):
        return self.printable_name

    @property
    def printable_name(self):
        return '{} #{}'.format(_('Order'), self.id)

    @property
    def full_name(self):
        return '{} {} {}'.format(
            self.last_name, self.first_name, self.middle_name)

    @property
    def total(self):
        return sum([i.subtotal for i in self.items.all()])

    @property
    def printable_total(self):
        return intcomma(self.total)

    def is_liqpay_payment(self):
        return self.is_paynow_form_visible() and apps.is_installed('liqpay')

    def is_paynow_form_visible(self):
        return self.payment_method.code == PAYMENT_METHOD_PRIVAT24

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderedProduct(models.Model):

    order = models.ForeignKey(
        Order,
        verbose_name=_('Order'),
        related_name='items',
        on_delete=models.CASCADE)

    product_id = models.IntegerField(_('Product ID'), blank=True, null=True)
    product_name = models.CharField(_("Product name"), max_length=255)
    product_code = models.CharField(_("Product code"), max_length=255)
    product_price = models.FloatField(_("Product price"))
    product_printable_price = models.CharField(
        _("Product printable price"), max_length=100)
    product_currency = models.PositiveIntegerField(_("Product currency"))
    product_logo = models.ImageField(
        _("Product logo"),
        blank=True,
        null=True,
        upload_to='ordered_product_logos'
    )

    qty = models.PositiveIntegerField(_('Quantity'), default=1)

    def __str__(self):
        return self.product_name

    @property
    def subtotal(self):
        return self.product_price * self.qty

    def printable_subtotal(self):
        return intcomma(self.subtotal)

    class Meta:
        verbose_name = _('Ordered product')
        verbose_name_plural = _('Ordered products')
