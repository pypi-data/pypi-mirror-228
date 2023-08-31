
from django.apps import apps
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _

from djmail import mail_managers


def get_new_order_context(order):
    return {
        'order': order,
        'title': '{} #{}'.format(_('New order'), order.id),
        'site': Site.objects.get_current(),
        'is_clothes_app_enabled': apps.is_installed('clothes')
    }


def send_new_order_sms(context):
    try:
        from turbosms import send_sms_from_template
        send_sms_from_template('orders/new_order_sms_for_manager.txt', context)
    except ImportError:
        pass
    except Exception as e:
        if settings.DEBUG:
            raise Exception('SMS sending error: {}'.format(e))


def send_new_order_email(context, subject=None):

    if subject is None:
        subject = context.get('title', '')

    html = render_to_string('orders/new_order_email_for_manager.html', context)

    mail_managers(subject, html)


def send_new_order_notifications(request, order):

    context = get_new_order_context(order)

    send_new_order_email(context)
    send_new_order_sms(context)
